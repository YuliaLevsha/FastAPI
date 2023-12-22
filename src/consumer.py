from json import loads
from aiokafka import AIOKafkaConsumer
from src.config import settings


class Consumer:
    def __init__(self, topic):
        self.consumer = AIOKafkaConsumer(topic,
                                         bootstrap_servers='localhost:9092',
                                         auto_offset_reset='earliest',
                                         value_deserializer=lambda x: loads(x.decode('utf-8'))
                                         )

    async def get_from_kafka(self, dao, param):
        result = []
        await self.consumer.start()
        try:
            async for message in self.consumer:
                message = await message.value
                if dao.get_all({}) is None:
                    dao.create_one(message)
                    result.append(settings.cache.connect().set(message.get(param), message))
                else:
                    if settings.cache.connect().get(message.get(param)) is None:
                        result.append(dao.get_one(message))
                    else:
                        result.append(settings.cache.connect().get(message.get(param)))
                print(message + ' было добавлено в монго.')
            return result
        finally:
            await self.consumer.stop()


consumer = Consumer('parsing')
