from datetime import datetime
import time
from fake_useragent import UserAgent
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Clothes(BaseModel):
    category: str
    gender: str
    name: str
    brand: str
    price: float
    data_instance: datetime

    def __str__(self):
        return "Category: " + self.category + ", " + "gender: " + self.gender + ", " + "name: " + self.name + "" \
                ", " + "brand: " + self.brand + ", " + "price: " + str(self.price) + ", " + "data: " + \
                self.data_instance.strftime('%Y-%m-%d %H:%M')


class LamodaScraper:
    def __init__(self):
        self.headers = {'User-Agent': UserAgent().chrome}

    async def get_page(self, url, num_page, session):
        page = await session.get(url + str(num_page), headers=self.headers)
        return page

    async def get_clothes(self, page):
        result = []
        html = await page.text()
        soup = BeautifulSoup(html, 'html.parser')

        i = 0
        for el in soup.select('.x-breadcrumbs__slide'):
            all_a = el.find('a', {"class": 'x-link__secondaryLabel'})
            if i == 1:
                gender = all_a.text.strip()
            elif i == 2:
                category = all_a.text.strip()
                break
            i = i + 1

        for clothes in soup.select('.x-product-card-description'):
            name = clothes.select('.x-product-card-description__product-name')
            brand = clothes.select('.x-product-card-description__brand-name')
            price = clothes.select('span')
            data = {'category': category,
                    'gender': gender,
                    'name': name[0].text,
                    'brand': brand[0].text,
                    'price': price[0].text,
                    'data_instance': datetime.now()}
            formatting = self.required_format(data)
            print(formatting)
            result.append(formatting)
        return result

    def required_format(self, data):
        float_price = data.get('price').split('р.')[0].replace(" ", "")
        data['price'] = float(float_price)
        clothes = Clothes(**data)
        return clothes

    async def fetch_all(self, urls):
        for url in urls:
            async with aiohttp.ClientSession() as session:
                tasks = []
                index = 1
                while True:
                    print("Page - " + str(index))
                    page = await self.get_page(url, index, session)
                    if len(await self.get_clothes(page)):
                        task = asyncio.ensure_future(self.get_clothes(page))
                        tasks.append(task)
                        index += 1
                    else:
                        break
                await asyncio.gather(*tasks)

    def fetch_async(self, urls):
        start = time.time()
        asyncio.run(self.fetch_all(urls))
        finish = time.time()
        print(str((finish-start) * 10**3) + "ms")
        return {'Status': 'good'}


# urls = ['https://www.lamoda.by/c/4418/clothes-body/?page=']
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# lamoda = LamodaScraper()
# lamoda.fetch_async(urls)
