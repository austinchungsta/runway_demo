"""
Some utils to parse the rss api payload and clean data
Payload: string: string representation of the json payload from the rss api
"""
from flask import jsonify
import json

def parse_rss(payload, app_id):
    data = json.loads(payload)
    reviews_data = data['feed']['entry']

    cleaned_data = []
    for review in reviews_data:
        cleaned_review = {
            'review_id': review['id']['label'],
            'app_id': app_id,
            'title': review['title']['label'],
            'review': review['content']['label'],
            'score': review['im:rating']['label'],
            'timestamp': review['updated']['label'],
            'author': review['author']['name']['label']
        }
        cleaned_data.append(cleaned_review)
    return cleaned_data
