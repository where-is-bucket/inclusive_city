import uuid
from dataclasses_json import dataclass_json
from dataclasses import dataclass
from uuid import UUID
from app.domain.author import Author
from app.domain.user import User


@dataclass
class Review:
    review_id: str
    author: Author
    review_text: str
    review_score: int

    @staticmethod
    def create(author: Author, review_text: str, review_score: int):
        return Review(
            review_id=str(uuid.uuid4()),
            author=author,
            review_text=review_text,
            review_score=review_score)