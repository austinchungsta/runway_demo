import React from 'react'

function Feed({ filteredReviews, hasError }) {
    if (hasError) {
        return (
            <div className="feed">
                <table className="styled-table">
                    <thead>
                        <tr>
                            <th>Review</th>
                            <th>Score</th>
                            <th>Time</th>
                            <th>Author</th>
                        </tr>
                    </thead>
                </table>
                <div className="body-message">
                    Error fetching reviews: Invalid ID or Network Error
                </div>
            </div>
        );
    }

    if (filteredReviews.length === 0) {
        return (
            <div className="feed">
                <table className="styled-table">
                    <thead>
                        <tr>
                            <th>Review</th>
                            <th className="td-score-text">Score</th>
                            <th>Time</th>
                            <th>Author</th>
                        </tr>
                    </thead>
                </table>
                <div className="body-message">
                    Query App ID to see reviews
                </div>
            </div>
        );
    }

    return (
        <div className="feed">
            <table className="styled-table">
                <thead>
                    <tr>
                        <th>Review</th>
                        <th className="td-score-text">Score</th>
                        <th>Time</th>
                        <th>Author</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredReviews.map((review, index) => (
                        <tr key={index}>
                            <td>
                                <h3>{review.title}</h3>
                                {review.review}
                            </td>
                            <td className="td-score-text">{review.score}</td>
                            <td>{review.timestamp}</td>
                            <td>{review.author}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );

}

export default Feed