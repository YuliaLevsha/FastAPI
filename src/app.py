from fastapi import FastAPI
from src.lamoda.lamoda_api import router as lamoda_router
from src.twitch.twitch_api import router as twitch_router


app = FastAPI()
app.include_router(lamoda_router)
app.include_router(twitch_router)


@app.get("/")
def hello():
    return {"Say": "Hello"}
