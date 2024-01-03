from json import loads
from kafka import KafkaConsumer


class Consumer:
    def __init__(self, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=["192.168.99.100:9092"],
            api_version=(2, 5, 0),
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            consumer_timeout_ms=10000,
            value_deserializer=lambda x: loads(x.decode("utf-8")),
        )

    def get_from_kafka(self, dao, partition, param):
        docs = []
        num = 1
        if len(list(dao.get_all({}))) == 0:
            for message in self.consumer:
                if message.partition == partition:
                    message = message.value
                    dao.create_one(message)
                    docs.append(message)
                    print(message, " было добавлено в монго.", num)
                    num += 1


consumer = Consumer("parsing")
