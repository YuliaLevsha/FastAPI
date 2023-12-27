import requests
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path
import redis

load_dotenv()


class MongoDbSettings(BaseSettings):
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    HOST: str

    def mongo_dsn(self):
        mongo_dsn = "mongodb://{0}:{1}@{2}:27017/?authMechanism=DEFAULT/".format(
            self.MONGO_INITDB_ROOT_USERNAME, self.MONGO_INITDB_ROOT_PASSWORD, self.HOST
        )
        return mongo_dsn


class TwitchAPISettings(BaseSettings):
    client_secret: str
    client_id: str

    def get_token(self):
        auth_url = "https://id.twitch.tv/oauth2/token"
        auth_params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        auth_response = requests.post(auth_url, params=auth_params)
        token = auth_response.json()["access_token"]
        return token


class RedisSettings(BaseSettings):
    HOST: str
    port: int = 6379

    def connect(self):
        connection = redis.asyncio.Redis(host=self.HOST, port=self.port, decode_responses=True)
        return connection


class Settings(BaseSettings):
    mongo_db: MongoDbSettings = MongoDbSettings(_env_file=Path('../.env'))
    twitch_api: TwitchAPISettings = TwitchAPISettings(_env_file=Path('../.env'))
    cache: RedisSettings = RedisSettings(_env_file=Path('../.env'))


settings = Settings()
