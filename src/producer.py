from json import dumps
from aiokafka import AIOKafkaProducer


class Producer:
    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=["192.168.99.100:9092"],
            api_version="2.5.0",
            value_serializer=lambda x: dumps(x).encode("utf-8"),
        )

    async def add_to_kafka(self, topic, data, partition):
        await self.producer.start()
        try:
            # breakpoint()
            for value in data:
                value = dict(value)
                value["data_instance"] = value.get("data_instance").strftime(
                    "%Y-%m-%dT%H:%M:%S.%f"
                )
                print(value)
                await self.producer.send_and_wait(
                    topic, value=value, partition=partition
                )
            await self.producer.flush()
            print("Все опубликовалось успешно!")
        finally:
            await self.producer.stop()


producer = Producer()
