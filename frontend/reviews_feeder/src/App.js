import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar.js';
import Feed from './components/Feed.js';

function App() {
  const [reviews, setReviews] = useState([]);
  const [filteredReviews, setFilteredReviews] = useState(reviews);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    // Set this to an empty page on startup
  }, [])

  return (
    <div className="container">
      <Sidebar filteredReviews={filteredReviews} setFilteredReviews={setFilteredReviews} reviews={reviews} setReviews={setReviews} setHasError={setHasError}></Sidebar>
      <Feed filteredReviews={filteredReviews} hasError={hasError}></Feed>
    </div>
  );
}

export default App;
