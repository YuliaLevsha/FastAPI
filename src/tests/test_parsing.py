import asyncio
from unittest.mock import patch, MagicMock
import aiohttp
from src.twitch.parser import TwitchScraper
from src.lamoda.parser import LamodaScraper
import unittest

data_twitch_test1 = {
    "data":
        {"id": "33214",
         "name": "Fortnite",
         "box_art_url": "https://static-cdn.jtvnw.net/ttv-boxart/33214-{width}x{height}.jpg",
         "igdb_id": "1905"}
}


class TestTwitchScraper(unittest.TestCase):
    @patch('src.twitch.parser.TwitchScraper.base_get_response', MagicMock(return_value=data_twitch_test1))
    async def test_base_get_response(self):
        result = TwitchScraper().base_get_response('games', {'id': 33214})
        print(result)
        self.assertEquals(result, data_twitch_test1)


class TestLamodaScrapper(unittest.TestCase):
    @patch('src.lamoda.parser.LamodaScraper.get_clothes', MagicMock(return_value=60))
    async def test_get_clothes(self):
        urls = ['https://www.lamoda.by/c/4418/clothes-body/?page=']
        lamoda = LamodaScraper()
        session = aiohttp.ClientSession()
        result = lamoda.get_clothes(await lamoda.get_page(urls[0], 1, session))
        print(result)
        await session.close()
        self.assertEquals(result, 60)


asyncio.run(TestTwitchScraper().test_base_get_response())
asyncio.run(TestLamodaScrapper().test_get_clothes())
