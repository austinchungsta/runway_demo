import os
import sys
from datetime import datetime, timedelta

# for local testing only -- when executing this file directly as main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.rss_parser import parse_rss
from config import API_BASE_URL, POSTGRES_CONNECTION_STRING

# Define the base model
Base = declarative_base()

# Define the table class
class AppReviews(Base):
    __tablename__ = 'app_reviews'
    id = Column(Integer, primary_key=True)
    review_id = Column(String(255))
    app_id = Column(String(255))
    title = Column(Text)
    review = Column(Text)
    score = Column(Integer)
    timestamp = Column(TIMESTAMP) # the app store API stores in UTC
    author = Column(String(255))

    @staticmethod
    def get_reviews(session, app_id, hour_filter=240):
        AppReviews.update_reviews(session, app_id)

        hour_filter = int(hour_filter) # if the hour filter parameter is explicitly passed, cast to int
        now = datetime.utcnow()
        lower_time_bound = now - timedelta(hours=hour_filter)
        recent_reviews = session.query(AppReviews).filter(
            AppReviews.app_id == app_id,
            AppReviews.timestamp >= lower_time_bound
        ).order_by(AppReviews.timestamp.desc()).all()

        recent_reviews_dicts = []
        for review in recent_reviews:
            review_dict = {column.name: getattr(review, column.name) for column in review.__table__.columns}
            recent_reviews_dicts.append(review_dict)

        # Below code calculates some metadata for the frontend

        metadata_review_count = len(recent_reviews_dicts)

        # For edge case when there have been no reviews in the specified time span
        if metadata_review_count == 0:
            return {
                'metadata': {
                    'review_count': 0,
                    'average_rating': 0,
                    'last_refresh': now,
                    'star_distribution': {str(star): 0 for star in range(1, 6)}
                },
                'reviews': None
            }
        metadata_average_rating = sum([float(review['score']) for review in recent_reviews_dicts])/metadata_review_count
        metadata_last_refresh = now

        # list comprehension to get the number of reviews for each star in a dict
        metadata_star_distribution = {str(star): sum(1 for review in recent_reviews_dicts if review['score'] == star) for star in range(1, 6)}

        return {
            'metadata': {
                    'review_count': metadata_review_count,
                    'average_rating': metadata_average_rating,
                    'last_refresh': metadata_last_refresh,
                    'star_distribution': metadata_star_distribution
                },
            'reviews': recent_reviews_dicts
            }

    @staticmethod
    def update_reviews(session, app_id):
        # Naive for now - just get the first page of reviews and batch upload to database
        uri = API_BASE_URL.format(app_id=app_id)

        try:

            # Get review data from API
            response = requests.get(uri)
            response.raise_for_status()
            reviews_data = parse_rss(response.text, app_id)

            # Get the entire list of reviews that we've already seen
            existing_reviews = []
            for review in session.query(AppReviews).filter(AppReviews.app_id == app_id).all():
                existing_reviews.append((review.review_id, review.app_id))

            for review in reviews_data:
                if (review['review_id'], review['app_id']) not in existing_reviews: # assumes that app_id review_id combination is unique
                    new_review = AppReviews(
                        review_id=review['review_id'],
                        app_id=review['app_id'],
                        title=review['title'],
                        review=review['review'],
                        score=review['score'],
                        timestamp=review['timestamp'],
                        author=review['author']
                    )
    
                    session.add(new_review)
            session.commit()
            return None
        except requests.RequestException as e:
            print(e)
            return None
    
    @staticmethod
    def update_scan(session):
        unique_app_ids = session.query(AppReviews.app_id).distinct().all()
        
        # Update reviews for each app
        for app_id_record in unique_app_ids:
            app_id = app_id_record[0]
            AppReviews.update_reviews(session, app_id)
        

# TODO: If this gets more complex, move to a central db connector file
# TODO: Error handling on the db connection
db_string = POSTGRES_CONNECTION_STRING

# connect to db and create the table
engine = create_engine(db_string)
Session = sessionmaker(bind=engine)
session = Session()

# run once to instantiate table
#Base.metadata.create_all(engine)