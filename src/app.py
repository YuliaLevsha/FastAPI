from fastapi import FastAPI, HTTPException
from src.lamoda.lamoda_api import router as lamoda_router
from src.twitch.twitch_api import router as twitch_router


app = FastAPI()
app.include_router(lamoda_router)
app.include_router(twitch_router)


@app.get("/")
def hello():
    return {"Say": "Hello"}


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    raise HTTPException(status_code=400, detail="Bad Request!")
