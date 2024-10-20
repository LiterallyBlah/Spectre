from playwright.async_api import async_playwright
import json
import os
from colorama import init, Fore, Style
from crawl.link_extractor import LinkExtractor
import asyncio

# Initialize colorama
init(autoreset=True)

# Constants
COOKIES_FILE = "output/cookies.json"

# Function to launch the browser interactively
async def launch_browser(headless=True):
    """Launches a browser instance interactively."""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless)
    return browser, playwright

# Function to create a new browser page
async def create_page(browser, width=1280, height=720):
    """
    Creates a new browser page with dynamic size.
    
    Args:
        browser: The browser instance.
        width (int): The width of the viewport in pixels. Default is 1280.
        height (int): The height of the viewport in pixels. Default is 720.
    
    Returns:
        A new page with the specified viewport size.
    """
    page = await browser.new_page()
    await page.set_viewport_size({"width": width, "height": height})
    return page

# Function to load cookies into a session
def load_cookies(page):
    """Loads cookies from a file to restore a session."""
    cookie_file = 'cookies.json'
    if os.path.exists(cookie_file) and os.path.getsize(cookie_file) > 0:
        try:
            with open(cookie_file, 'r') as f:
                cookies = json.load(f)
            page.context.add_cookies(cookies)
            print(f"{Fore.GREEN}Cookies loaded successfully.{Style.RESET_ALL}")
        except json.JSONDecodeError:
            print(f"{Fore.YELLOW}Warning: Cookie file is not valid JSON. Skipping cookie loading.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error loading cookies: {str(e)}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No cookie file found or file is empty. Continuing without cookies.{Style.RESET_ALL}")

# Function to save cookies from the session
async def save_cookies(page, cookies_file=COOKIES_FILE):
    """Saves cookies to a file to preserve a session."""
    try:
        cookies = await page.context.cookies()
        with open(cookies_file, 'w') as f:
            json.dump(cookies, f)
        print(f"{Fore.GREEN}Cookies saved to {cookies_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}Failed to save cookies: {str(e)}{Style.RESET_ALL}")

# Function to navigate to a URL
async def navigate_to_page(page, url):
    """Navigates to a specific URL."""
    await page.goto(url)
    print(f"{Fore.CYAN}Navigated to {url}{Style.RESET_ALL}")

# Function to handle an interactive session
async def handle_interactive_session(url, headless=False):
    """Manages an interactive browser session."""
    print(f"{Fore.YELLOW}Starting interactive session...{Style.RESET_ALL}")
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=headless)
        page = await create_page(browser)

        load_cookies(page)  # Load session cookies if available
        await navigate_to_page(page, url)  # Navigate to the desired URL

        # Create a LinkExtractor instance
        headless_browser = await playwright.chromium.launch(headless=True)
        link_extractor = LinkExtractor(headless_browser)

        try:
            while True:
                command = input(f"{Fore.GREEN}Enter command (navigate/extract/exit): {Style.RESET_ALL}").strip().lower()
                
                if command == 'navigate':
                    new_url = input(f"{Fore.YELLOW}Enter URL to navigate to: {Style.RESET_ALL}")
                    await navigate_to_page(page, new_url)
                elif command == 'extract':
                    print(f"{Fore.CYAN}Extracting links from the current page...{Style.RESET_ALL}")
                    links_map = await link_extractor.extract_links(page, page.url)
                    print(f"{Fore.GREEN}Extracted links:{Style.RESET_ALL}")
                    for url, status in links_map.items():
                        status_color = Fore.GREEN if status == 200 else Fore.YELLOW
                        print(f"  {status_color}{url} (Status: {status}){Style.RESET_ALL}")
                elif command == 'exit':
                    break
                else:
                    print(f"{Fore.RED}Invalid command. Please use 'navigate', 'extract', or 'exit'.{Style.RESET_ALL}")
        finally:
            await save_cookies(page)  # Save session cookies before closing
            await headless_browser.close()
            await browser.close()

    return None, None  # Return None for both browser and playwright

# Function to close the browser
async def close_browser(browser, playwright):
    """Closes the browser and stops the Playwright instance."""
    if browser:
        await browser.close()

# # Example usage
# if __name__ == "__main__":
#     handle_interactive_session("https://example.com", headless=False)
