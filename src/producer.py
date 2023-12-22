from json import dumps
from aiokafka import AIOKafkaProducer


class Producer:
    def __init__(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=['localhost:9092'],
                                         value_serializer=lambda x: dumps(x).encode('utf-8')
                                         )

    async def add_to_kafka(self, topic, data, partition):
        self.producer.start()
        try:
            for value in data:
                print(dict(value))
                self.producer.send(topic, value=dict(value), partition=partition)
            # await self.producer.flush()
            print('Все опубликовалось успешно!')
        finally:
            await self.producer.stop()


producer = Producer()
