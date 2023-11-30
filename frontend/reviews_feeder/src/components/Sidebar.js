import React, { useEffect, useState } from 'react';
import { API_ENDPOINTS } from '../config';
function Sidebar({ filteredReviews, setFilteredReviews, reviews, setReviews, setHasError }) {

    // Props and constants
    const MAX_DAYS = 10;
    const [daysFilter, setDaysFilter] = useState(10);
    const [inputValue, setInputValue] = useState('');
    const [starFilter, setStarFilter] = useState(5);
    const [reviewCount, setReviewCount] = useState(0);
    const [averageRating, setAverageRating] = useState("N/A");
    const [lastRefresh, setLastRefresh] = useState("N/A");

    // Event handlers and effects
    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    // Update the ratings bar whenever the filters change
    useEffect(() => {
        updateRatingsChart();
    }, [filteredReviews]);

    // Main API call
    const fetchReviewsData = (app_id) => {
        let hours = MAX_DAYS * 24;
        const url = `${API_ENDPOINTS.GET_REVIEWS}?app_id=${app_id}&hours=${hours}`; //TODO: refactor out endpoint

        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .catch(error => {
                console.error("Error fetching data: ", error);
                throw error;
            });
    };

    // TODO: refactor out a lot of the below utility functions into a sidebar utils file

    const handleSearchClick = () => {
        fetchReviewsData(inputValue)
            .then(payload => {
                setHasError(false);
                // Update all the props with the new data
                let fetchedReviews = payload.reviews;
                setReviews(fetchedReviews);
                let filteredByStar = applyStarFilter(fetchedReviews, starFilter);
                let filteredByDay = applyDayFilter(filteredByStar, daysFilter);
                setFilteredReviews(filteredByDay);
                let metadata = payload.metadata;
                setAverageRating(parseFloat(metadata.average_rating).toFixed(2));
                setLastRefresh(metadata.last_refresh);
            })
            .catch(error => {
                setHasError(true);
                console.error("Error in handleSearchClick: ", error);
            });
    };

    const updateMetadata = (filteredReviews) => {
        const reviewCount = filteredReviews.length;
        const averageRating = filteredReviews.reduce((acc, review) => acc + review.score, 0) / reviewCount;

        setReviewCount(reviewCount);
        setAverageRating(reviewCount > 0 ? averageRating.toFixed(2) : "N/A");
    };

    const applyStarFilter = (reviews, starFilter) => {
        const filteredReviews = reviews.filter(review => review.score <= starFilter);
        updateMetadata(filteredReviews);
        return filteredReviews;
    };

    const applyDayFilter = (reviews, daysFilter) => {
        const timeLimit = new Date();
        timeLimit.setDate(timeLimit.getDate() - daysFilter);
        const filteredReviews = reviews.filter(review => {
            const reviewDate = new Date(review.timestamp);
            return reviewDate >= timeLimit;
        });
        updateMetadata(filteredReviews);
        return filteredReviews;
    };

    const handleStarFilterChange = (event) => {
        const newStarFilter = parseInt(event.target.value, 0); // Magic number for number of stars
        setStarFilter(newStarFilter);
        const updatedFilteredReviews = applyStarFilter(reviews, newStarFilter);
        setFilteredReviews(updatedFilteredReviews);
    };

    const handleDayFilterChange = (event) => {
        const newDaysFilter = parseInt(event.target.value, MAX_DAYS);
        setDaysFilter(newDaysFilter);
        const updatedFilteredReviews = applyDayFilter(reviews, newDaysFilter);
        setFilteredReviews(updatedFilteredReviews);
    };

    // Helper function for updating the ratings bar
    function updateRatingsChart() {
        const reviewData = filteredReviews.reduce((acc, review) => {
            const starCount = review.score;
            acc[starCount] = (acc[starCount] || 0) + 1;
            return acc;
        }, {});

        const maxReviews = Math.max(...Object.values(reviewData));

        document.querySelectorAll('.rating').forEach(ratingEl => {
            const stars = ratingEl.getAttribute('data-stars');
            const reviews = reviewData[stars] || 0;
            const widthPercent = (reviews / maxReviews) * 100;
            ratingEl.querySelector('.bar').style.width = `${widthPercent}%`;
        });
    }

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <h1>Reviews</h1>
            </div>
            <div className="sidebar-body">
                <div className="searchbar">
                    <input
                        type="text"
                        placeholder="App ID Search"
                        value={inputValue}
                        onChange={handleInputChange}
                    />
                    <button
                        className="search-button"
                        onClick={handleSearchClick}
                    >
                        Search
                    </button>
                </div>

                <div className="filters">
                    <div className="filter">
                        <label>Show reviews from: {daysFilter} days ago</label>
                        <input
                            type="range"
                            min="1"
                            max="10"
                            value={daysFilter}
                            onChange={handleDayFilterChange}
                        />
                    </div>
                    <div className="filter">
                        <label>Show reviews with up to: {starFilter} stars</label>
                        <input
                            type="range"
                            min="1"
                            max="5"
                            value={starFilter}
                            onChange={handleStarFilterChange}
                        />
                    </div>
                </div>
                <div className="app-header">
                    <h2>App Reviews Overview</h2>
                </div>
                <div className="stats">
                    <div id="star-ratings">
                        <div className="rating" data-stars="5"><span>★★★★★</span> <div className="bar"></div></div>
                        <div className="rating" data-stars="4"><span>★★★★☆</span> <div className="bar"></div></div>
                        <div className="rating" data-stars="3"><span>★★★☆☆</span> <div className="bar"></div></div>
                        <div className="rating" data-stars="2"><span>★★☆☆☆</span> <div className="bar"></div></div>
                        <div className="rating" data-stars="1"><span>★☆☆☆☆</span> <div className="bar"></div></div>
                    </div>
                </div>
                <div className="metadata">
                    <div className="metadata-item">
                        <span>
                            <p className="metadata-large-font">Review Count: </p>
                            <p className="metadata-small-font">{reviewCount}</p>
                        </span>
                    </div>
                    <div className="metadata-item">
                        <p className="metadata-large-font">Average Rating: </p>
                        <p className="metadata-small-font">{averageRating}</p>
                    </div>
                    <div className="metadata-item">
                        <p className="metadata-large-font">Last Refresh: </p>
                        <p className="metadata-smaller-font">{lastRefresh}</p>
                    </div>
                </div>
                <div className="time-toggle"></div>
                <div className=""></div>
            </div>
        </div>
    );
}

export default Sidebar