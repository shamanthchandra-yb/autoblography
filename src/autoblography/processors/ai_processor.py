"""
AI processing utilities including Kapa AI integration
"""

import requests
from typing import List, Tuple, Optional

from ..config.settings import settings


class AIProcessor:
    """AI processing utilities"""
    
    def __init__(self, kapa_api_key: Optional[str] = None, kapa_base_url: Optional[str] = None):
        """
        Initialize AI processor
        
        Args:
            kapa_api_key: Kapa AI API key. If not provided, uses KAPA_API_KEY from settings
            kapa_base_url: Kapa AI base URL. If not provided, uses KAPA_BASE_URL from settings
        """
        self.kapa_api_key = kapa_api_key or settings.kapa_api_key
        self.kapa_base_url = kapa_base_url or settings.kapa_base_url
        
        # Default Kapa AI project ID (you may want to make this configurable)
        self.kapa_project_id = "5e2862a7-aeac-4a87-8593-c1fd2842a7cd"

    def post_kapa_ai(self, query_text: str) -> requests.Response:
        """
        Sends a query to the Kapa AI API and returns the response object.
        
        Args:
            query_text: Query text to send to Kapa AI
            
        Returns:
            Response object from Kapa AI API
        """
        if not self.kapa_api_key:
            raise ValueError("Kapa AI API key is required. Set KAPA_API_KEY environment variable or pass kapa_api_key parameter.")
        
        url = f"{self.kapa_base_url}/query/v1/projects/{self.kapa_project_id}/chat/"

        headers = {
            "X-API-KEY": self.kapa_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "query": query_text
        }

        response = requests.post(url, headers=headers, json=payload)
        return response

    def get_relevant_existing_blogs(self, query_text: str) -> Optional[List[Tuple[str, str]]]:
        """
        Queries Kapa AI for relevant existing blogs based on the provided text.
        
        Args:
            query_text: Query text to find relevant blogs
            
        Returns:
            List of tuples (url, title) or None if error
        """
        formatted_query = f"""
        I am writing a blog for below. Give existing documentation and blogs links only. It should be with key, value pair (value pair being link) only, on what resources would be helpful to link here. Don't add anything else.
        {query_text}
        """

        response = self.post_kapa_ai(formatted_query)

        if response.ok:
            response_json = response.json()
            sources = []
            for item in response_json.get('relevant_sources', []):
                try:
                    sources.append((item['source_url'], item['title']))
                except Exception:
                    continue  # Skip item if any error occurs
            return sources
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None 