import React, {useCallback, useEffect, useState} from "react";
import ReviewRow from "./components/ReviewRow/index.jsx";
import {FiEdit3} from "react-icons/fi";
import AddReviewForm from "./components/AddReviewForm/index.jsx";

const ReviewsTab = ({selectedMarker, refetchPlace}) => {
    const [reviews, setReviews] = useState(selectedMarker.reviews);
    const [isLoadingReviews, setIsLoadingReviews] = useState(false);
    const [showForm, setShowForm] = useState(false);

    const fetchReviews = useCallback(async () => {
        setIsLoadingReviews(true);
        try {
            const response = await refetchPlace(selectedMarker.place_id);
            setReviews(response.data.reviews);
        } finally {
            setIsLoadingReviews(false);
        }
    }, [refetchPlace, selectedMarker.place_id]);

    useEffect(() => {
        if (selectedMarker?.reviews) {
            setReviews(selectedMarker.reviews)
        }
    }, [selectedMarker]);

    return (
        <div className="comments">
            <div className="comments__header">
                <div className="comments__title">Відгуки</div>
                <button
                    className="comments__add-btn"
                    onClick={() => setShowForm(!showForm)}
                >
                    <FiEdit3 size={16} />
                    <span>Залишити відгук</span>
                </button>
            </div>

            {showForm && (
                <AddReviewForm
                    selectedMarker={selectedMarker}
                    fetchReviews={fetchReviews}
                    hideForm={() => setShowForm(false)}
                />
            )}

            {isLoadingReviews ? (
                <div className="comments__loader">
                    <div className="spinner"></div>
                </div>
            ) : reviews.length === 0 ? (
                <p className="comments__empty">Ще немає відгуків</p>
            ) : (
                <ul className="comments__list">
                    {reviews.map((review) => (
                        <ReviewRow review={review} key={review.review_id}/>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default ReviewsTab;