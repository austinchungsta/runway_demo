import json

from flask import Flask, jsonify, request
from flask_cors import CORS

from models.reviews_model import AppReviews, session

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get request for fetching review data for a given application
@app.route('/get_reviews')
def get_reviews():
    app_id = request.args.get('app_id')
    hour_filter = request.args.get('hours')
    if not app_id:
        return jsonify({'error': 'app_id not provided'}), 400
    if not hour_filter:
        return jsonify({'error': 'hours parameter not provided'}), 400
    
    reviews = AppReviews.get_reviews(session, app_id, hour_filter=hour_filter)
    return(jsonify(reviews))

if __name__ == '__main__':
    app.run(debug=True)