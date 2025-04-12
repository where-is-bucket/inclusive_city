import uvicorn
from fastapi import FastAPI

from app.api.v1.review_router import router as review_router
from app.api.v1.place_router import router as place_router
from app.api.v1.facility_router import router as proposal_router

app = FastAPI(title="inclusive_city")

v1  = "/api/v1"
# app.include_router(user_router, prefix=v1)
app.include_router(review_router, prefix=v1)
app.include_router(place_router, prefix=v1)
app.include_router(proposal_router, prefix=v1)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)