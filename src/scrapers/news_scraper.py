from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

class NewsScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return ""

    def parse_article(self, article_html: str) -> Dict:
        """To be implemented by specific scrapers"""
        raise NotImplementedError

    def search_articles(self, keywords: List[str], max_articles: int = 5) -> List[Dict]:
        """To be implemented by specific scrapers"""
        raise NotImplementedError 