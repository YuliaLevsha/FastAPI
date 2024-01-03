import requests
from config import settings
from twitch.twitch_model import Games, Streams, Streamers
from datetime import datetime


class TwitchScraper:
    def __init__(self):
        self.base_url = "https://api.twitch.tv/helix/"
        self.headers = {
            "client-id": settings.twitch_api.client_id,
            "Authorization": f"Bearer {settings.twitch_api.get_token()}",
        }

    async def base_get_response(self, query, fields):
        response = requests.get(
            self.base_url + query, headers=self.headers, params=fields
        )
        return response.json()

    async def get_games(self):
        games = []
        json_data = await self.base_get_response("games/top", {"first": 100})
        for game in json_data.get("data"):
            data = {"name": game.get("name"), "data_instance": datetime.now()}
            game_ = Games(**data)
            games.append(game_)
        return games

    async def get_streams(self):
        streams = []
        list_users_id = []
        fields = {"first": 100}
        json_data = await self.base_get_response("streams", fields)
        for stream in json_data.get("data"):
            data = {
                "stream_name": stream.get("title"),
                "streamer_name": stream.get("user_login"),
                "game_name": stream.get("game_name"),
                "viewers": stream.get("viewer_count"),
                "data_instance": datetime.now(),
            }
            list_users_id.append(stream.get("user_id"))
            stream_ = Streams(**data)
            streams.append(stream_)
        return list_users_id, streams

    async def get_streamers(self):
        streamers = []
        users = await self.get_streams()
        for user in users[0]:
            json_data = await self.base_get_response("users", {"id": user})
            json_data = json_data.get("data")[0]
            data_create = json_data.get("created_at")
            data = {
                "login": json_data.get("login"),
                "name": json_data.get("display_name"),
                "data_create": datetime.strptime(data_create, "%Y-%m-%dT%H:%M:%SZ"),
                "data_instance": datetime.now(),
            }
            streamer = Streamers(**data)
            streamers.append(streamer)
        return streamers
