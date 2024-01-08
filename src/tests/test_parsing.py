from unittest.mock import patch, MagicMock
import aiohttp
import pytest
from bs4 import BeautifulSoup
from src.twitch.twitch_parser import TwitchScraper
from src.lamoda.lamoda_parser import LamodaScraper
from src.config import settings

data_twitch_test1 = {
    "data": {
        "id": "33214",
        "name": "Fortnite",
        "box_art_url": "https://static-cdn.jtvnw.net/ttv-boxart/33214-{width}x"
        "{height}.jpg",
        "igdb_id": "1905",
    }
}

URL = settings.urls[0]


def html_text():
    with open("src/tests/html_text_lamoda.txt", "r", encoding="utf-8") as file:
        text = file.read()
    return BeautifulSoup(text, "html.parser").text.replace("\n", "")[:50]


@pytest.mark.asyncio
async def test_base_get_response():
    with patch(
        "src.twitch.twitch_parser.TwitchScraper.base_get_response",
        MagicMock(return_value=data_twitch_test1),
    ):
        scrapper = TwitchScraper()
        result = scrapper.base_get_response("games", {"id": 33215})
        assert result == data_twitch_test1


@pytest.mark.asyncio
async def test_get_clothes():
    with patch(
        "src.lamoda.lamoda_parser.LamodaScraper.get_clothes", MagicMock(return_value=60)
    ):
        scrapper = LamodaScraper()
        async with aiohttp.ClientSession() as session:
            result = scrapper.get_clothes(await scrapper.get_page(URL, 1, session))
            assert result == 60


@pytest.mark.asyncio
async def test_beautifulSoup():
    with patch("bs4.BeautifulSoup", MagicMock(return_value=html_text())):
        scrapper = LamodaScraper()
        async with aiohttp.ClientSession() as session:
            page = await scrapper.get_page(URL, 1, session)
            html = await page.text()
            result = BeautifulSoup(html, "html.parser").text.replace("\n", "")[:50]
            assert result == html_text()
