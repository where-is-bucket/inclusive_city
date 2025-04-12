from pydantic import BaseModel

class AddReviewRequest(BaseModel):
    place_id: str
    author_name: str
    comment: str
    rating: int

class AddReviewResponse(BaseModel):
    review_id: str