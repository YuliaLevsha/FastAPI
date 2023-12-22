from .twitch_parser import TwitchScraper
from fastapi import Depends, APIRouter
from src.producer import producer
from src.dao import DAO
from src.consumer import consumer

router = APIRouter(prefix='/twitch')


@router.get('/games-parser')
async def scrapper_games(scraper: TwitchScraper = Depends()):
    games = await scraper.get_games()
    await producer.add_to_kafka('parsing', data=games, partition=1)
    return {'Games': 'ok'}


@router.get('/streams-parser')
async def scrapper_streams(scraper: TwitchScraper = Depends()):
    streams = await scraper.get_streams()
    await producer.add_to_kafka('parsing', streams)
    return {'Streams': 'ok'}


@router.get('/streamers-parser')
async def scrapper_streamers(scraper: TwitchScraper = Depends()):
    streamers = await scraper.get_streamers()
    await producer.add_to_kafka('parsing', streamers)
    return {'Streamers': 'ok'}


@router.get('/get-games')
async def get_games():
    dao = DAO('games')
    data = await consumer.get_from_kafka(dao, 'name')
    return {'Games:': data}


def get_streams():
    pass


def get_streamers():
    pass
