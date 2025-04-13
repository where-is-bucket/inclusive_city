import React from "react";
import { FaStar, FaRegStar } from "react-icons/fa";

const ReviewRow = ({ review }) => {
    const rating = review.rating || 0;
    const fullStars = Math.floor(rating);
    const emptyStars = 5 - fullStars;

    return (
        <li className="comments__item">
            <div className="comments__header">
                <div className="comments__author">{review.author.author_name}</div>
                {rating > 0 && (
                    <div className="comments__rating">
                        {[...Array(fullStars)].map((_, i) => (
                            <FaStar key={`full-${i}`} className="star-icon filled" />
                        ))}
                        {[...Array(emptyStars)].map((_, i) => (
                            <FaRegStar key={`empty-${i}`} className="star-icon" />
                        ))}
                    </div>
                )}
            </div>
            <div className="comments__text">{review.review_text}</div>
            {review.created_at && (
                <div className="comments__date">
                    {new Date(review.created_at).toLocaleDateString()}
                </div>
            )}
        </li>
    );
};

export default ReviewRow;