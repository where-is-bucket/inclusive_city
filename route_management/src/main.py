from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

@app.get("/route")
async def get_route():
    return jsonable_encoder({"test": "test"})