
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.di import get_place_repository
from app.domain.author import Author
from app.domain.review import Review
from app.infrastructure.mongoPlaceRepository import MongoPlaceRepository
from app.schemas.addReview import AddReviewRequest, AddReviewResponse


router = APIRouter()

@router.post("/reviews", response_model=AddReviewResponse)
async def add_review(
    request: AddReviewRequest,
    place_repository: MongoPlaceRepository = Depends(get_place_repository)):

    place = await place_repository.get_by_id(request.place_id)

    if place == None:
        raise HTTPException(status_code=404)
    
    try:
        author = Author(author_name=request.author_name)

        review = Review.create(
            author= author,
            review_text=request.comment,
            review_score=request.rating)
        
        place.add_review(review)

        await place_repository.save(place);
    
        return AddReviewResponse(review_id=review.review_id)

    except Exception:
        raise HTTPException(status_code=400)
    
# @router.get("/reviews")
# def get_all_reviews(
#     place_id: int,
#     place_repository: MongoPlaceRepository = Depends(MongoPlaceRepository)):

#     place = place_repository.get_by_id(place_id);

#     if place == None:
#         raise HTTPException(status_code=404)


#     return place.reviews;
