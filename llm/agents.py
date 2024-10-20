import ollama
from colorama import Fore, Style

class LinkValidationAgent:
    def __init__(self, model="llama3.1"):
        self.model = model

    def validate_links(self, links: list, base_url: str) -> list:
        """Validates links using LLM analysis."""
        system_prompt = "You are an AI assistant specialized in analyzing and validating URLs."
        user_prompt = f"Analyze the following list of URLs and return only the valid ones that belong to the domain {base_url}. URLs:\n{links}"
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ])
            result = response['message']['content'].strip()
            validated_links = [link.strip() for link in result.split('\n') if link.strip()]
            return validated_links
        except Exception as e:
            print(f"{Fore.RED}Error in LLM validation: {str(e)}{Style.RESET_ALL}")
            return links  # Return original links if LLM validation fails

class LinkExtractionAgent:
    def __init__(self, model="llama3.1"):
        self.model = model

    def extract_links(self, content: str, content_type: str, base_url: str) -> list:
        """Extracts links from code and text using LLM analysis."""
        system_prompt = "You are an AI assistant specialized in identifying and extracting URLs from various types of content, including code and text. Your output should be a bulleted list of URLs or an empty response if no URLs are found."
        user_prompt = f"""
        Analyze the following content and extract all potential URLs or references to web resources. 
        The content type is: {content_type}
        The base URL is: {base_url}

        Please return ONLY a list of extracted URLs or references. Include both absolute and relative URLs.
        If no URLs or references are found, only return 'false'.



        Content:
        {content[:1000]}

        ==================================================
        Output format:
        - URL1
        - URL2
        - URL3
        Please return the output in the specified format and respond with 'false' if no URLs are found. Only conclusive urls will be allowed. Do not include any other text.
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ])
            result = response['message']['content'].strip()
            extracted_links = [link.strip() for link in result.split('\n') if link.strip()]
            return extracted_links
        except Exception as e:
            print(f"{Fore.RED}Error in LLM link extraction: {str(e)}{Style.RESET_ALL}")
            return []  # Return an empty list if LLM extraction fails
