from src.lamoda.lamoda_parser import LamodaScraper
from src.producer import producer
from fastapi import Depends, APIRouter
from src.consumer import consumer
from src.dao import DAO
from src.config import settings

router = APIRouter(prefix="/lamoda")
dao = DAO("clothes")


@router.get("/clothes-parser")
async def scrapper_clothes(scraper: LamodaScraper = Depends()):
    clothes = await scraper.fetch_all(settings.urls)
    await producer.add_to_kafka("parsing", data=clothes, partition=0)
    return {"Clothes": "ok"}


@router.get("/get-clothes")
async def get_clothes():
    data = consumer.get_from_kafka(partition=0)
    result = await consumer.mongo_redis(
        docs=data, dao=dao, param="name", collection_name="clothes"
    )
    return {"Clothes:": result}
