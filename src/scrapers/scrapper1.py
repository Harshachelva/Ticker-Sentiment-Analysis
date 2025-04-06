import sqlite3
import requests
from bs4 import BeautifulSoup
import re


def clean_text(text):
    """Clean and preprocess text."""
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    text = text.lower().strip()  
    return text


def initialize_db(db_name="articles.db"):
    """Initialize the SQLite database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            title TEXT UNIQUE,
            url TEXT UNIQUE,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_article_to_db(ticker, title, url, content, db_name="articles.db"):
    """Save article data into the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO articles (ticker, title, url, content)
            VALUES (?, ?, ?, ?)
        ''', (ticker, title, url, content))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Duplicate article skipped: {title}")
    conn.close()


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

    initialize_db()
    keywords = ["Tata Motors", "HDFC"]

    for keyword in keywords:
        print(f"Fetching articles for: {keyword}")
        articles = search_finshots_articles(keyword) 
        for article in articles:
            title = clean_text(article["title"])
            url = article["url"]
            content = fetch_article_content(url)
            save_article_to_db(keyword, title, url, content)


if __name__ == "__main__":
    main()
