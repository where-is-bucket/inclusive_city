from pydantic import BaseModel

class CreateReviewRequest(BaseModel):
    place_id: str
    author_name: str
    comment: str
    rating: int

class CreateReviewResponse(BaseModel):
    review_id: str