from src.twitch.twitch_parser import TwitchScraper
from fastapi import Depends, APIRouter
from src.producer import producer
from src.dao import DAO
from src.consumer import consumer

router = APIRouter(prefix="/twitch")


@router.get("/games-parser")
async def scrapper_games(scraper: TwitchScraper = Depends()):
    games = await scraper.get_games()
    await producer.add_to_kafka("parsing", data=games, partition=1)
    return {"Games": "ok"}


@router.get("/streams-parser")
async def scrapper_streams(scraper: TwitchScraper = Depends()):
    streams = await scraper.get_streams()
    await producer.add_to_kafka("parsing", data=streams[1], partition=2)
    return {"Streams": "ok"}


@router.get("/streamers-parser")
async def scrapper_streamers(scraper: TwitchScraper = Depends()):
    streamers = await scraper.get_streamers()
    await producer.add_to_kafka("parsing", data=streamers, partition=3)
    return {"Streamers": "ok"}


@router.get("/get-games")
async def get_games():
    dao = DAO("games")
    data = consumer.get_from_kafka(partition=1)
    result = await consumer.mongo_redis(
        docs=data, dao=dao, param="name", collection_name="games"
    )
    return {"Games:": result}


@router.get("/get-streams")
async def get_streams():
    dao = DAO("streams")
    data = consumer.get_from_kafka(partition=2)
    result = await consumer.mongo_redis(
        docs=data, dao=dao, param="stream_name", collection_name="streams"
    )
    return {"Streams:": result}


@router.get("/get-streamers")
async def get_streamers():
    dao = DAO("streamers")
    data = consumer.get_from_kafka(partition=3)
    result = await consumer.mongo_redis(
        docs=data, dao=dao, param="name", collection_name="streamers"
    )
    return {"Streamers:": result}
