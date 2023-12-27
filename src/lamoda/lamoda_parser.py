from datetime import datetime
from fake_useragent import UserAgent
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from src.lamoda.lamoda_model import Clothes


class LamodaScraper:
    def __init__(self):
        self.headers = {"User-Agent": UserAgent().chrome}

    async def get_page(self, url, num_page, session):
        page = await session.get(url + str(num_page), headers=self.headers)
        return page

    async def get_clothes(self, page):
        result = []
        html = await page.text()
        soup = BeautifulSoup(html, "html.parser")

        category = soup.select(".x-breadcrumbs__slide > a")[3]
        gender = soup.select(".x-breadcrumbs__slide > a")[1]

        for clothes in soup.select(".x-product-card-description"):
            name = clothes.select(".x-product-card-description__product-name")
            brand = clothes.select(".x-product-card-description__brand-name")
            price = clothes.select("span")
            data = {
                "category": category.text.strip(),
                "gender": gender.text.strip(),
                "name": name[0].text,
                "brand": brand[0].text,
                "price": price[0].text,
                "data_instance": datetime.now(),
            }
            formatting = self.required_format(data)
            result.append(formatting)
        return result

    def required_format(self, data):
        float_price = data.get("price").split("р.")[0].replace(" ", "")
        data["price"] = float(float_price)
        clothes = Clothes(**data)
        return clothes

    async def fetch_all(self, urls):
        result = []
        for url in urls:
            async with aiohttp.ClientSession() as session:
                tasks = []
                index = 1
                while True:
                    page = await self.get_page(url, index, session)
                    if len(await self.get_clothes(page)):
                        task = asyncio.ensure_future(self.get_clothes(page))
                        tasks.append(task)
                        index += 1
                    else:
                        break
                values = await asyncio.gather(*tasks)
                for value in values:
                    result.extend(value)
                return result
