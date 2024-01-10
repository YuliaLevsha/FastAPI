from fastapi import FastAPI, HTTPException
from src.lamoda.lamoda_api import router as lamoda_router
from src.twitch.twitch_api import router as twitch_router
from src.producer import producer


app = FastAPI()
app.include_router(lamoda_router)
app.include_router(twitch_router)


@app.get("/")
def hello():
    return {"Say": "Hello"}


@app.exception_handler(TypeError)
async def exception_handler(request, exc):
    raise HTTPException(status_code=428, detail="Необходимо пропарсить данные!")


@app.on_event('shutdown')
async def close_producer():
    await producer.producer.stop()
