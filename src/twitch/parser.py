import requests
import src.credentials as credentials
from datetime import datetime
import aiohttp
import asyncio
from pydantic import BaseModel


def get_token():
    auth_url = 'https://id.twitch.tv/oauth2/token'
    auth_params = {'client_id': credentials.client_id,
                   'client_secret': credentials.client_secret,
                   'grant_type': 'client_credentials'}

    auth_response = requests.post(auth_url, params=auth_params)
    token = auth_response.json()['access_token']
    return token


class Streams(BaseModel):
    stream_name: str
    streamer_name: str
    game_name: str
    viewers: int
    data_instance: datetime

    def __str__(self):
        return "Stream name: " + self.stream_name + ", " + "streamer name: " + self.streamer_name + ", " + "" \
                "game name: " + self.game_name + ", " + "viewers: " + str(self.viewers) + ", " + "data: " + \
                self.data_instance.strftime('%Y-%m-%d %H:%M')


class Games(BaseModel):
    name: str
    data_instance: datetime

    def __str__(self):
        return "Name: " + self.name + ", " + "data: " + self.data_instance.strftime('%Y-%m-%d %H:%M')


class Streamers(BaseModel):
    login: str
    name: str
    data_create: datetime
    data_instance: datetime

    def __str__(self):
        return "Login: " + self.login + ", " + "name: " + self.name + ", " + "data create: " + \
            self.data_create.strftime('%Y-%m-%d %H:%M') + ", " + "data instance: " + \
            self.data_instance.strftime('%Y-%m-%d %H:%M')


class TwitchScraper:
    def __init__(self):
        self.base_url = 'https://api.twitch.tv/helix/'
        self.headers = {'client-id': credentials.client_id,
                        'Authorization': f'Bearer {get_token()}'}

    async def base_get_response(self, query, fields):
        response = requests.get(self.base_url + query, headers=self.headers, params=fields)
        return response.json()

    async def get_games(self):
        games = []
        json_data = await self.base_get_response('games/top', {'first': 100})
        for game in json_data.get('data'):
            data = {
                'name': game.get('name'),
                'data_instance': datetime.now()
            }
            game_ = Games(**data)
            games.append(game_)
        for game in games:
            print(game)
        return games

    async def get_streams(self):
        streams = []
        list_users_id = []
        fields = {'first': 100}
        # while True:
        #     json_data = self.base_get_response('streams', fields)
        #     for stream in json_data.get('data'):
        #         streams.append(stream)
        #         print(stream)
        #     cursor = json_data['pagination']['cursor']
        #     if cursor:
        #         fields['after'] = cursor
        #     else:
        #         break
        json_data = await self.base_get_response('streams', fields)
        for stream in json_data.get('data'):
            data = {
                'stream_name': stream.get('title'),
                'streamer_name': stream.get('user_login'),
                'game_name': stream.get('game_name'),
                'viewers': stream.get('viewer_count'),
                'data_instance': datetime.now()
            }
            list_users_id.append(stream.get('user_id'))
            stream_ = Streams(**data)
            streams.append(stream_)
        for stream in streams:
            print(stream)
        return list_users_id, streams

    async def get_streamers(self):
        streamers = []
        users = await self.get_streams()
        for user in users[0]:
            json_data = await self.base_get_response('users', {'id': user})
            json_data = json_data.get('data')[0]
            data_create = json_data.get('created_at')
            data = {
                'login': json_data.get('login'),
                'name': json_data.get('display_name'),
                'data_create': datetime.strptime(data_create, '%Y-%m-%dT%H:%M:%SZ'),
                'data_instance': datetime.now()
            }
            streamer = Streamers(**data)
            streamers.append(streamer)
        for streamer in streamers:
            print(streamer)
        return streamers


# twitch = TwitchScraper()
# asyncio.run(twitch.base_get_response('games', {'id': 33214}))
