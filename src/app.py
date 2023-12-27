from fastapi import FastAPI
from kafka import KafkaClient, KafkaAdminClient
from kafka.admin import NewTopic

from src.lamoda.api import router as lamoda_router
from src.twitch.api import router as twitch_router


app = FastAPI()
app.include_router(lamoda_router)
app.include_router(twitch_router)


# @app.on_event("startup")
# async def create_topic_if_not_exists():
#     bootstrap_servers = ['192.168.99.100:9092']
#     client = KafkaClient(
#         bootstrap_servers=bootstrap_servers,
#         api_version=(2, 5, 0)
#     )
#     admin_client = KafkaAdminClient(
#         bootstrap_servers=bootstrap_servers,
#         api_version=(2, 5, 0)
#     )
#
#     future = client.cluster.request_update()
#     client.poll(future=future)
#     metadata = client.cluster
#     print(metadata.topics())
#     if 'parsing' not in metadata.topics():
#         topic = NewTopic(name='parsing', num_partitions=4, replication_factor=1)
#         admin_client.create_topics(new_topics=[topic], validate_only=False)


@app.get("/")
def hello():
    return {"Say": "Hello"}
