from fastapi import FastAPI
from kafka import KafkaClient, KafkaAdminClient
from kafka.admin import NewTopic

from src.lamoda.api import router as lamoda_router
from src.twitch.api import router as twitch_router


app = FastAPI()
app.include_router(lamoda_router)
app.include_router(twitch_router)


@app.get("/")
def hello():
    return {"Say": "Hello"}
