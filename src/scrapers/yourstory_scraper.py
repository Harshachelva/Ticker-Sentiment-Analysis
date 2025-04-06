from bs4 import BeautifulSoup
from typing import List, Dict
from .news_scraper import NewsScraper
import requests

class YourStoryScraper(NewsScraper):
    def __init__(self):
        super().__init__("https://yourstory.com")
        self.search_url = "https://yourstory.com/search"
        
    def search_articles(self, keywords: List[str], max_articles: int = 5) -> List[Dict]:
        articles = []
        
        for keyword in keywords:
            params = {"q": keyword}
            self.logger.info(f"Fetching articles for: {keyword}")
            
            try:
                response = requests.get(self.search_url, params=params, headers=self.headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                article_cards = soup.select('div.article-card, div.MuiGrid-item')[:max_articles]

                print(f"Fetched these articles for {keyword}")
                for idx, card in enumerate(article_cards, start=1):
                    link = card.find('a')
                    if not link:
                        continue
                        
                    url = link.get('href', '')
                    if not url.startswith('http'):
                        url = f"https://yourstory.com{url}"
                    
                    title = link.get_text().strip()
                    print(f"{idx}. {title} - {url}")
                    
                    article_html = self.fetch_page(url)
                    if article_html:
                        article_data = self.parse_article(article_html)
                        article_data.update({
                            'url': url,
                            'keyword': keyword,
                            'title': title
                        })
                        articles.append(article_data)
                        
                if not article_cards:
                    print(f"No articles found for {keyword}")
                    
            except requests.RequestException as e:
                self.logger.error(f"Error fetching articles for {keyword}: {str(e)}")
                continue

        return articles

    def parse_article(self, article_html: str) -> Dict:
        soup = BeautifulSoup(article_html, 'html.parser')
        
        content_area = soup.select_one('.article-content, .global-content-typography')
        content = ""
        if content_area:
            paragraphs = content_area.find_all('p')
            content = " ".join(p.get_text().strip() for p in paragraphs)
        
        date_elem = soup.select_one('time, .article-date')
        date = date_elem.get_text().strip() if date_elem else ""

        return {
            'content': content,
            'date': date,
            'source': 'YourStory'
        }