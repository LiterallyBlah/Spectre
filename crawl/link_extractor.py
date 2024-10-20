import re
from urllib.parse import urljoin, urlparse
from playwright.async_api import Page, Browser
from colorama import Fore, Style
import io
import PyPDF2
from llm.agents import LinkExtractionAgent
import json
import asyncio

class LinkExtractor:
    def __init__(self, browser: Browser, model="qwen2.5", window_size=20000, step_size=10000):
        self.window_size = window_size
        self.step_size = step_size
        self.extraction_agent = LinkExtractionAgent(model)
        self.browser = browser

    async def extract_links(self, page: Page, base_url: str) -> list:
        """
        Extracts links from the current page using a combination of regex, LLM analysis, and validation.
        
        Args:
            page (Page): The Playwright page object.
            base_url (str): The base URL of the current domain.
        
        Returns:
            list: A list of unique, valid URLs within the current domain.
        """
        print(f"{Fore.CYAN}Extracting links from the current page...{Style.RESET_ALL}")
        
        # Step 1: Determine the content type and extract content
        content_type = await page.evaluate("() => document.contentType")
        content = await self._extract_content(page, content_type)
        
        # Step 2: Extract links based on content type using chunking and LLM
        raw_links = self._extract_links_chunked(content, content_type, base_url)
        
        # Step 3: Validate links
        validated_links = await self._validate_links(raw_links, base_url, page)
        
        # Remove duplicates from the validated_links map
        unique_validated_links = {url: status for url, status in validated_links.items()}
        
        return unique_validated_links

    async def _extract_content(self, page: Page, content_type: str) -> str:
        """Extracts content based on the content type."""
        if content_type.startswith('text/') or content_type in ['application/xml', 'application/xhtml+xml']:
            return await page.content()
        elif content_type == 'application/pdf':
            pdf_buffer = io.BytesIO(await page.pdf())
            pdf_reader = PyPDF2.PdfReader(pdf_buffer)
            return ' '.join(page.extract_text() for page in pdf_reader.pages)
        else:
            return await page.inner_text()  # Fallback to extracting visible text

    def _extract_links_chunked(self, content: str, content_type: str, base_url: str) -> list:
        """Extracts links using chunking for all content types."""
        all_links = []
        total_chunks = (len(content) - self.window_size) // self.step_size + 1
        processed_chunks = 0

        for i in range(0, len(content), self.step_size):
            chunk = content[i:i+self.window_size]
            
            # Use regex for initial extraction
            if content_type.startswith('text/html') or content_type in ['application/xml', 'application/xhtml+xml']:
                chunk_links = self._extract_links_regex(chunk, base_url)
            else:
                chunk_links = self._extract_links_text(chunk, base_url)
            
            # Use LLM for additional extraction
            llm_links = [link[2:] for link in self.extraction_agent.extract_links(chunk, content_type, base_url) if link.startswith('- ') and 'false' not in link.lower()]
            llm_links = [link.lstrip('- ') for link in llm_links]

            # Combine links
            all_links.extend(chunk_links + llm_links)
            
            processed_chunks += 1
            progress = (processed_chunks / total_chunks) * 100
            print(f"\r{Fore.CYAN}Link extraction progress: {progress:.2f}%", end="", flush=True)

        print(f"\n{Fore.GREEN}Link extraction complete.")
        return list(set(all_links))  # Remove duplicates

    def _extract_links_regex(self, content: str, base_url: str) -> list:
        """Extracts links using regex for HTML and XML content."""
        link_pattern = re.compile(r'(?:href|src)=[\'"]?([^\'" >]+)')
        links = link_pattern.findall(content)
        return [urljoin(base_url, link) for link in links]

    def _extract_links_text(self, content: str, base_url: str) -> list:
        """Extracts links from plain text content."""
        link_pattern = re.compile(r'https?://\S+')
        links = link_pattern.findall(content)
        return links

    async def _validate_links(self, links: list, base_url: str, page: Page) -> dict:
        """Validates links by checking domain and attempting to navigate in headless mode."""
        link_status_map = {}
        original_headers = await page.evaluate("() => JSON.stringify(Object.fromEntries(window.performance.getEntriesByType('navigation')[0].serverTiming.map(e => [e.name, e.description])))")
        original_headers = json.loads(original_headers)

        # Extract the protocol from the base_url
        base_url_parts = urlparse(base_url)
        base_protocol = base_url_parts.scheme

        context = await self.browser.new_context()
        try:
            for link in links:
                # Parse the link
                parsed_link = urlparse(link)
                
                # If the link doesn't have a scheme (protocol), use the base_url's scheme
                if not parsed_link.scheme:
                    link = f"{base_protocol}:{link}" if link.startswith("//") else urljoin(base_url, link)
                
                if self._is_same_domain(link, base_url):
                    link_status_map[link] = 200  # Assume 200 OK for same domain
                else:
                    try:
                        new_page = await context.new_page()
                        await new_page.set_extra_http_headers(original_headers)
                        response = await new_page.goto(link, wait_until="domcontentloaded", timeout=5000)
                        if response:
                            link_status_map[link] = response.status
                        else:
                            link_status_map[link] = None  # No response
                        await new_page.close()
                    except Exception as e:
                        print(f"{Fore.YELLOW}Failed to validate link: {link}. Error: {str(e)}{Style.RESET_ALL}")
                        link_status_map[link] = None  # Error occurred
        finally:
            await context.close()

        return link_status_map

    def _is_same_domain(self, link: str, base_url: str) -> bool:
        """Checks if the link belongs to the same domain as the base URL."""
        link_domain = urlparse(link).netloc
        base_domain = urlparse(base_url).netloc
        return link_domain == base_domain or link_domain == ''
