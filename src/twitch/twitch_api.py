from twitch.twitch_parser import TwitchScraper
from fastapi import Depends, APIRouter
from producer import producer
from dao import DAO
from consumer import consumer

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
def get_games():
    dao = DAO("games")
    consumer.get_from_kafka(dao, partition=1, param="games")
    return {"Games:": "good"}


@router.get("/get-streams")
def get_streams():
    dao = DAO("streams")
    consumer.get_from_kafka(dao, partition=2, param="streams")
    return {"Streams:": "good"}


@router.get("/get-streamers")
def get_streamers():
    dao = DAO("streamers")
    consumer.get_from_kafka(dao, partition=3, param="streamers")
    return {"Streamers:": "good"}
