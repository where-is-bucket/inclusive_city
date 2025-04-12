from fastapi import APIRouter, Depends

from app.domain.location import Location
from app.domain.place import Place
from app.domain.user import User

router = APIRouter()

@router.get("/users", response_model=str)
def create_user():
    
    # user = User(0, 'John Doe', 'ocherednyara');

    # location = Location(1, 1);
    # place = Place(1, "House of the pain", location);

    # aggregate = ReviewAggregate.create(place);

    # aggregate.add_review(user, 1, "Hello world")

    return "Helo world"
    
