import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  // ✅ Root of the current deployment (works locally or in proxy)
  const root_url = window.location.origin + '/';

  const { id } = useParams();

  // ✅ Use root_url instead of hardcoded proxy URLs
  const dealer_url  = `${root_url}djangoapp/dealer/${id}/`;
  const reviews_url = `${root_url}djangoapp/reviews/dealer/${id}/`;
  const post_review = `${root_url}postreview/${id}/`;

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const retobj = await res.json();
      if (retobj.status === 200) {
        let dealerobjs = Array.from(retobj.dealer);
        setDealer(dealerobjs[0]);
      }
    } catch (err) {
      console.error("Dealer fetch failed:", err);
    }
  };

  const get_reviews = async () => {
    try {
      const res = await fetch(reviews_url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const retobj = await res.json();
      if (retobj.status === 200) {
        setReviews(retobj.reviews || []);
        setUnreviewed((retobj.reviews || []).length === 0);
      }
    } catch (err) {
      console.error("Review fetch failed:", err);
      setUnreviewed(true); // gracefully show “No reviews”
    }
  };

  const senti_icon = (sentiment) => {
    return sentiment === "positive"
      ? positive_icon
      : sentiment === "negative"
      ? negative_icon
      : neutral_icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(
        <a href={post_review}>
          <img
            src={review_icon}
            style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }}
            alt='Post Review'
          />
        </a>
      );
    }
  }, []); // runs once when component mounts

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        <h1 style={{ color: "grey" }}>
          {dealer.full_name}{postReview}
        </h1>
        <h4 style={{ color: "grey" }}>
          {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
        </h4>
      </div>

      <div className="reviews_panel">
        {reviews.length === 0 && unreviewed === false ? (
          <div>Loading Reviews....</div>
        ) : unreviewed === true ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map((review, idx) => (
            <div key={idx} className="review_panel">
              <img
                src={senti_icon(review.sentiment)}
                className="emotion_icon"
                alt='Sentiment'
              />
              <div className="review">{review.review}</div>
              <div className="reviewer">
                {review.name} {review.car_make} {review.car_model} {review.car_year}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;
