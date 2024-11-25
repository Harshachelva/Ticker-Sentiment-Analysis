import sqlite3
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    #ToDo: Additional cleaning,prepping  things
    return text


def initialize_db(db_name="articles.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            title TEXT UNIQUE,
            url TEXT UNIQUE,
            content TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_article_to_db(ticker, title, url, content, date, db_name="articles.db"):
    """Save article data into the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO articles (ticker, title, url, content, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (ticker, title, url, content, date))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Duplicate article skipped: {title}")
    conn.close()

def search_finshots_articles(keyword):

    search_url = "https://backend.finshots.in/backend/search/"

    params = {"q": keyword}
    
   
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }
    
    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()  
        data = response.json()
        articles = data.get("matches")[:5] 
        results=[]
        print(f"Fetched these articles for {keyword}")
        for idx, article in enumerate(articles, start=1):
            url = article.get("post_url")  
            title = article.get("title")   
            if title and url:
                results.append({"title": title, "url": url})
                print(f"{idx}. {article['title']} - {article['post_url']}")
            else:
                print(f"No articles found for {keyword}")
            
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Finshots: {e}")
        return []

def fetch_article_content(url):
    """Fetch the content of an article from its URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join(p.get_text() for p in paragraphs)
        return clean_text(content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article content from {url}: {e}")
        return ""


def main():
    #ToDo: Append if table created
    initialize_db()
    tickers = ["Tata Motors", "HDFC"]

    for ticker in tickers:
        print(f"Fetching articles for: {ticker}")
        articles = search_finshots_articles(ticker)  
        for article in articles:
            title = clean_text(article["title"])
            url = article["url"]
            content = fetch_article_content(url)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
            save_article_to_db(ticker, title, url, content, date)


if __name__ == "__main__":
    main()