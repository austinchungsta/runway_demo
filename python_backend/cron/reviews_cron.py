#!/usr/bin/env python3

from models.reviews_model import AppReviews, session

# for local testing only -- when executing this file directly as main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def poll_reviews();
    """
    Cron Job that polls the ios reviews rss feed for new reviews
    Default should probably be one poll every hour
    Todo: Take care of pagination
    """
    AppReviews.update_scan(session)
