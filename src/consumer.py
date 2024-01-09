from json import loads
from kafka import KafkaConsumer
from src.config import settings


class Consumer:
    def __init__(self, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=settings.kafka.bootstrap_service(),
            api_version=(2, 5, 0),
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            consumer_timeout_ms=10000,
            value_deserializer=lambda x: loads(x.decode("utf-8")),
        )

    def get_from_kafka(self, partition):
        docs = []
        for message in self.consumer:
            if message.partition == partition:
                message = message.value
                docs.append(message)
        return docs

    async def mongo_redis(self, docs, dao, param, collection_name):
        if dao.check_db():
            for doc in docs:
                params = {param: doc.get(param)}
                dao.update(params, data=doc)
            result_cache = await settings.cache.connect().get(collection_name)
            if not result_cache:
                await settings.cache.connect().set(collection_name, str(docs), ex=1200)
                result_cache = await settings.cache.connect().get(collection_name)
            print("----Cache----")
            return result_cache
        else:
            dao.create_many(docs)
            await settings.cache.connect().set(collection_name, str(docs), ex=1200)
            print("----Mongo----")
            return list(dao.get_all({}))


consumer = Consumer("parsing")
