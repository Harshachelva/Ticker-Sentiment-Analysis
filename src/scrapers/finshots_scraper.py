from bs4 import BeautifulSoup
from typing import List, Dict
from .news_scraper import NewsScraper
import re

class FinshotsScraper(NewsScraper):
    def __init__(self):
        super().__init__("https://finshots.in")
        ##self.search_url = "https://finshots.in/?s={}"
        self.search_url = "https://backend.finshots.in/backend/search/"

    def parse_article(self, article_html: str) -> Dict:
        soup = BeautifulSoup(article_html, 'html.parser')
        
        # Extract title
        title_elem = soup.find('h1', class_='entry-title')
        title = title_elem.text.strip() if title_elem else ""

        # Extract content
        content_elem = soup.find('div', class_='entry-content')
        content = content_elem.text.strip() if content_elem else ""

        # Extract date
        date_elem = soup.find('time', class_='entry-date')
        date = date_elem.text.strip() if date_elem else ""

        return {
            'title': title,
            'content': content,
            'date': date,
            'source': 'Finshots'
        }

    def search_articles(self, keywords: List[str], max_articles: int = 5) -> List[Dict]:
        articles = []
        for keyword in keywords:
            search_url = self.search_url.format(keyword)
            html = self.fetch_page(search_url)
            if not html:
                continue

            soup = BeautifulSoup(html, 'html.parser')
            article_links = soup.find_all('a', href=re.compile(r'/archive/'))
            
            for link in article_links[:max_articles]:
                article_url = link['href']
                article_html = self.fetch_page(article_url)
                if article_html:
                    article_data = self.parse_article(article_html)
                    article_data['url'] = article_url
                    article_data['keyword'] = keyword
                    articles.append(article_data)

        return articles 