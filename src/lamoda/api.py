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
    clothes = await scraper.fetch_all(urls)
    await producer.add_to_kafka('parsing', data=clothes, partition=0)
    return {'Clothes': 'ok'}


@router.get('/get-clothes')
def get_clothes():
    consumer.get_from_kafka(dao, partition=0, param='clothes')
    return {'Clothes:': 'good'}
