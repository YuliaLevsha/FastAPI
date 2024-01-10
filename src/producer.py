from json import dumps
from aiokafka import AIOKafkaProducer
from src.config import settings
from datetime import datetime
import logging


class Producer:
    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka.bootstrap_service(),
            api_version="2.5.0",
            value_serializer=lambda x: dumps(x).encode("utf-8"),
        )

    async def add_to_kafka(self, topic, data, partition):
        await self.producer.start()
        for value in data:
            value = dict(value)
            for key in value:
                if isinstance(value.get(key), datetime):
                    value[key] = value.get(key).strftime("%Y-%m-%dT%H:%M:%S.%f")
            await self.producer.send(topic, value=value, partition=partition)
        logging.info("Все опубликовалось успешно!")


producer = Producer()
