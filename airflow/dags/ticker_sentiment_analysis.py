from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import json
from sqlalchemy import create_engine
import logging
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from scrapers.finshots_scraper import FinshotsScraper
from scrapers.yourstory_scraper import YourStoryScraper

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'ticker_sentiment_analysis',
    default_args=default_args,
    description='Scrape, clean and analyze sentiment for tickers',
    schedule_interval='0 19 * * 1-5',  # 7 PM every working day
    start_date=days_ago(1),
    catchup=False,
)

# Keywords to search for
TICKERS = ['HDFC', 'Tata Motors']

# Function to scrape Finshots
def scrape_finshots():
    logging.info("Starting Finshots scraping")
    scraper = FinshotsScraper()
    articles = scraper.search_articles(TICKERS, max_articles=5)
    
    # Save to temporary storage
    df = pd.DataFrame(articles)
    df.to_csv('/opt/airflow/data/finshots_raw.csv', index=False)
    logging.info("Finshots scraping completed")

# Function to scrape YourStory
def scrape_yourstory():
    logging.info("Starting YourStory scraping")
    scraper = YourStoryScraper()
    articles = scraper.search_articles(TICKERS, max_articles=5)
    
    # Save to temporary storage
    df = pd.DataFrame(articles)
    df.to_csv('/opt/airflow/data/yourstory_raw.csv', index=False)
    logging.info("YourStory scraping completed")

# Function to clean Finshots data
def clean_finshots_data():
    logging.info("Cleaning Finshots data")
    df = pd.read_csv('/opt/airflow/data/finshots_raw.csv')
    
    # Basic cleaning steps
    df['title'] = df['title'].str.strip()
    df['content'] = df['content'].str.strip()
    df['date'] = pd.to_datetime(df['date'])
    df = df.drop_duplicates(subset=['title'])
    
    # Save cleaned data
    df.to_csv('/opt/airflow/data/finshots_cleaned.csv', index=False)
    logging.info("Finshots data cleaning completed")

# Function to clean YourStory data
def clean_yourstory_data():
    logging.info("Cleaning YourStory data")
    df = pd.read_csv('/opt/airflow/data/yourstory_raw.csv')
    
    # Basic cleaning steps
    df['title'] = df['title'].str.strip()
    df['content'] = df['content'].str.strip()
    df['date'] = pd.to_datetime(df['date'])
    df = df.drop_duplicates(subset=['title'])
    
    # Save cleaned data
    df.to_csv('/opt/airflow/data/yourstory_cleaned.csv', index=False)
    logging.info("YourStory data cleaning completed")

# Function to perform sentiment analysis
def analyze_sentiment():
    logging.info("Starting sentiment analysis")
    
    # Read cleaned data
    finshots_df = pd.read_csv('/opt/airflow/data/finshots_cleaned.csv')
    yourstory_df = pd.read_csv('/opt/airflow/data/yourstory_cleaned.csv')
    
    # Combine data
    combined_df = pd.concat([finshots_df, yourstory_df])
    
    # Mock sentiment analysis (replace with actual API call)
    def get_sentiment(text):
        # This is a mock function - replace with actual sentiment analysis API
        return 0.5  # Mock sentiment score between 0 and 1
    
    combined_df['sentiment_score'] = combined_df['content'].apply(get_sentiment)
    
    # Save results
    combined_df.to_csv('/opt/airflow/data/sentiment_results.csv', index=False)
    
    # Store in database
    engine = create_engine('postgresql://airflow:airflow@postgres/airflow')
    combined_df.to_sql('sentiment_analysis', engine, if_exists='append', index=False)
    
    logging.info("Sentiment analysis completed")

# Define tasks
scrape_finshots_task = PythonOperator(
    task_id='scrape_finshots',
    python_callable=scrape_finshots,
    dag=dag,
)

scrape_yourstory_task = PythonOperator(
    task_id='scrape_yourstory',
    python_callable=scrape_yourstory,
    dag=dag,
)

clean_finshots_task = PythonOperator(
    task_id='clean_finshots_data',
    python_callable=clean_finshots_data,
    dag=dag,
)

clean_yourstory_task = PythonOperator(
    task_id='clean_yourstory_data',
    python_callable=clean_yourstory_data,
    dag=dag,
)

analyze_sentiment_task = PythonOperator(
    task_id='analyze_sentiment',
    python_callable=analyze_sentiment,
    dag=dag,
)

# Define task dependencies
[scrape_finshots_task, scrape_yourstory_task] >> clean_finshots_task
[scrape_finshots_task, scrape_yourstory_task] >> clean_yourstory_task
[clean_finshots_task, clean_yourstory_task] >> analyze_sentiment_task 