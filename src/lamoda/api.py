from .lamoda_parser import LamodaScraper
from src.producer import producer
from fastapi import Depends, APIRouter
from src.consumer import consumer
from src.dao import DAO

urls = ['https://www.lamoda.by/c/4418/clothes-body/?page=']
router = APIRouter(prefix='/lamoda')
dao = DAO('clothes')


@router.get('/clothes-parser')
async def scrapper_clothes(scraper: LamodaScraper = Depends()):
    clothes = scraper.fetch_async(urls)
    producer.add_to_kafka('parsing', clothes)
    return {'Clothes': 'ok'}


@router.post('/get-clothes')
async def get_clothes():
    consumer.get_from_kafka(dao)
    # result = consumer.get_from_kafka(dao)
    return {'Clothes:': 'ok'}
