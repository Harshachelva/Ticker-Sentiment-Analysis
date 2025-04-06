from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    content = Column(Text)
    source = Column(String(100))
    url = Column(String(500))
    keyword = Column(String(100))
    sentiment_score = Column(Float)
    date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseHandler:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.logger = logging.getLogger(__name__)

    def save_articles(self, articles: list):
        try:
            for article in articles:
                db_article = Article(
                    title=article['title'],
                    content=article['content'],
                    source=article['source'],
                    url=article['url'],
                    keyword=article['keyword'],
                    sentiment_score=article['sentiment_score'],
                    date=datetime.strptime(article['date'], '%Y-%m-%d') if article['date'] else None
                )
                self.session.add(db_article)
            
            self.session.commit()
            self.logger.info(f"Successfully saved {len(articles)} articles")
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Error saving articles: {str(e)}")
            raise

    def get_latest_articles(self, keyword: str, limit: int = 5):
        try:
            return self.session.query(Article)\
                .filter(Article.keyword == keyword)\
                .order_by(Article.created_at.desc())\
                .limit(limit)\
                .all()
        except Exception as e:
            self.logger.error(f"Error fetching articles: {str(e)}")
            raise

    def close(self):
        self.session.close() 