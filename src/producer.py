from json import dumps
from kafka import KafkaProducer
from src.config import settings
from datetime import datetime


class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.kafka.bootstrap_service(),
            api_version="2.5.0",
            value_serializer=lambda x: dumps(x).encode("utf-8"),
        )

    def add_to_kafka(self, topic, data, partition):
        for value in data:
            value = dict(value)
            for key in value:
                if isinstance(value.get(key), datetime):
                    value[key] = value.get(key).strftime("%Y-%m-%dT%H:%M:%S.%f")
            print(value)
            self.producer.send(topic, value=value, partition=partition)
        print("Все опубликовалось успешно!")


producer = Producer()
