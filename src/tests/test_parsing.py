import asyncio
from unittest.mock import patch, MagicMock
import aiohttp
from bs4 import BeautifulSoup
from twitch.twitch_parser import TwitchScraper
from lamoda.lamoda_parser import LamodaScraper
import unittest

data_twitch_test1 = {
    "data": {
        "id": "33214",
        "name": "Fortnite",
        "box_art_url": "https://static-cdn.jtvnw.net/ttv-boxart/33214-{width}x"
        "{height}.jpg",
        "igdb_id": "1905",
    }
}


def html_text():
    with open("tests/html_text_lamoda.txt", "r", encoding="utf-8") as file:
        text = file.read()
    return BeautifulSoup(text, "html.parser").text.replace("\n", "")[:50]


class TestTwitchScraper(unittest.TestCase):
    @patch(
        "twitch.twitch_parser.TwitchScraper.base_get_response",
        MagicMock(return_value=data_twitch_test1),
    )
    async def test_base_get_response(self):
        result = TwitchScraper().base_get_response("games", {"id": 33214})
        self.assertEquals(result, data_twitch_test1)


class TestLamodaScrapper(unittest.TestCase):
    @patch("lamoda.lamoda_parser.LamodaScraper.get_clothes", MagicMock(return_value=60))
    async def test_get_clothes(self):
        urls = ["https://www.lamoda.by/c/4418/clothes-body/?page="]
        lamoda = LamodaScraper()
        session = aiohttp.ClientSession()
        result = lamoda.get_clothes(await lamoda.get_page(urls[0], 1, session))
        await session.close()
        self.assertEquals(result, 60)

    @patch("bs4.BeautifulSoup", MagicMock(return_value=html_text()))
    async def test_beautifulSoup(self):
        urls = ["https://www.lamoda.by/c/4418/clothes-body/?page="]
        session = aiohttp.ClientSession()
        page = await LamodaScraper().get_page(urls[0], 1, session)
        html = await page.text()
        result = BeautifulSoup(html, "html.parser").text.replace("\n", "")[:50]
        await session.close()
        self.assertEquals(result, html_text())


async def fetch_all():
    task1 = asyncio.ensure_future(TestTwitchScraper().test_base_get_response())
    task2 = asyncio.ensure_future(TestLamodaScrapper().test_get_clothes())
    task3 = asyncio.ensure_future(TestLamodaScrapper().test_beautifulSoup())
    tasks = [task1, task2, task3]
    await asyncio.gather(*tasks)


asyncio.run(fetch_all())
