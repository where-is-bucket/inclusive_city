import React, {useState} from "react";
import {addReview} from "../../../../../..//api/places-api.js";
import {FaStar} from "react-icons/fa";

const AddReviewForm = ({selectedMarker, fetchReviews, hideForm}) => {
    const [authorName, setAuthorName] = useState("");
    const [commentText, setCommentText] = useState("");
    const [isLoadingSubmit, setIsLoadingSubmit] = useState(false);
    const [rating, setRating] = useState(0);
    const [hoverRating, setHoverRating] = useState(0);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!authorName.trim() || !commentText.trim()) return;

        setIsLoadingSubmit(true);
        try {
            await addReview({
                payload: {
                    place_id: selectedMarker.place_id,
                    author_name: authorName,
                    comment: commentText,
                    rating: rating > 0 ? rating : null // Відправляємо рейтинг, якщо він вибраний
                }
            });
            setAuthorName("");
            setCommentText("");
            setRating(0);
            await fetchReviews();
            hideForm();
        } finally {
            setIsLoadingSubmit(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="comments__form">
            <div className="comments__form-group">
                <input
                    type="text"
                    value={authorName}
                    onChange={(e) => setAuthorName(e.target.value)}
                    className="comments__form-input"
                    placeholder="Ваше ім'я"
                    required
                    disabled={isLoadingSubmit}
                />
            </div>

            <div className="comments__form-group" style={{marginBottom: '0'}}>
                <textarea
                    value={commentText}
                    onChange={(e) => setCommentText(e.target.value)}
                    className="comments__form-textarea"
                    placeholder="Ваш відгук"
                    rows="3"
                    required
                    disabled={isLoadingSubmit}
                />
            </div>

            <div className="comments__form-group">
                <div className="rating-stars">
                    {[1, 2, 3, 4, 5].map((star) => (
                        <span
                            key={star}
                            className="star"
                            onMouseEnter={() => setHoverRating(star)}
                            onMouseLeave={() => setHoverRating(0)}
                            onClick={() => setRating(star)}
                        >
                            {(hoverRating || rating) >= star ? (
                                <FaStar className="star-icon filled"/>
                            ) : (
                                <FaStar className="star-icon outlined"/>
                            )}
                        </span>
                    ))}
                </div>
            </div>

            <div className="comments__form-actions">
                <button
                    type="button"
                    className="comments__cancel-btn"
                    onClick={hideForm}
                    disabled={isLoadingSubmit}
                >
                    Скасувати
                </button>
                <button
                    type="submit"
                    className="comments__submit-btn"
                    disabled={isLoadingSubmit}
                >
                    {isLoadingSubmit ? (
                        <>
                            <span className="comments__spinner"></span>
                            Відправка...
                        </>
                    ) : (
                        "Надіслати"
                    )}
                </button>
            </div>
        </form>
    );
}

export default AddReviewForm;