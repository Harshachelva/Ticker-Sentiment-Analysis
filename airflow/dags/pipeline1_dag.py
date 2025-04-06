from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.scrapers.yourstory_scraper import YourStoryScraper
from src.scrapers.finshots_scraper import FinshotsScraper
from src.sentiment.sentiment_analyzer import SentimentAnalyzer
from src.processors.database_handler import DatabaseHandler
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def scrape_and_analyze():
    # Initialize components
    yourstory_scraper = YourStoryScraper()
    finshots_scraper = FinshotsScraper()
    sentiment_analyzer = SentimentAnalyzer()
    
    # Database connection string from environment variable
    db_connection = os.getenv('DATABASE_URL', 'postgresql://airflow:airflow@postgres/airflow')
    db_handler = DatabaseHandler(db_connection)

    try:
        # Keywords to search for
        keywords = ['HDFC', 'Tata Motors']
        
        # Scrape articles
        yourstory_articles = yourstory_scraper.search_articles(keywords)
        finshots_articles = finshots_scraper.search_articles(keywords)
        
        # Combine articles
        all_articles = yourstory_articles + finshots_articles
        
        # Analyze sentiment
        analyzed_articles = sentiment_analyzer.analyze_articles(all_articles)
        
        # Save to database
        db_handler.save_articles(analyzed_articles)
        
    finally:
        db_handler.close()

dag = DAG(
    'pipeline1_news_sentiment',
    default_args=default_args,
    description='Pipeline for scraping news and analyzing sentiment',
    schedule_interval='0 19 * * 1-5',  # Run at 7 PM on weekdays
    start_date=datetime(2024, 1, 1),
    catchup=False,
)

scrape_and_analyze_task = PythonOperator(
    task_id='scrape_and_analyze',
    python_callable=scrape_and_analyze,
    dag=dag,
) 