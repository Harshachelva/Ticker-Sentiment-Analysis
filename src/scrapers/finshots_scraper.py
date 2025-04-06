import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from .news_scraper import NewsScraper
import re

class FinshotsScraper(NewsScraper):
    def __init__(self):
        super().__init__("https://finshots.in")
        self.search_url = "https://backend.finshots.in/backend/search/"
        
    def search_articles(self, keywords: List[str], max_articles: int = 5) -> List[Dict]:
        articles = []
        
        for keyword in keywords:
            params = {"q": keyword}
            self.logger.info(f"Fetching articles for: {keyword}")
            
            try:
                response = requests.get(self.search_url, params=params, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                matches = data.get("matches", [])[:max_articles]
                
                print(f"Fetched these articles for {keyword}")
                for idx, article in enumerate(matches, start=1):
                    url = article.get("post_url")
                    title = article.get("title")
                    
                    if title and url:
                        print(f"{idx}. {title} - {url}")
                        article_html = self.fetch_page(url)
                        if article_html:
                            article_data = self.parse_article(article_html)
                            article_data.update({
                                'url': url,
                                'keyword': keyword,
                                'title': title,
                                'date': article.get('published_date', '')
                            })
                            articles.append(article_data)
                    else:
                        print(f"No articles found for {keyword}")
                        
            except requests.RequestException as e:
                self.logger.error(f"Error fetching articles for {keyword}: {str(e)}")
                continue

        return articles

    def parse_article(self, article_html: str) -> Dict:
        soup = BeautifulSoup(article_html, 'html.parser')
        
        title_elem = soup.find('h1', class_='entry-title')
        title = title_elem.text.strip() if title_elem else ""

        content_elem = soup.find('div', class_='entry-content')
        content = content_elem.text.strip() if content_elem else ""
        
        date_elem = soup.find('time', class_='entry-date')
        date = date_elem.text.strip() if date_elem else ""

        return {
            'title': title,
            'content': content,
            'date': date,
            'source': 'Finshots'
        }
