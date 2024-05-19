import os
import json
import time

import aiohttp
import asyncio

from bs4 import BeautifulSoup
from pprint import pprint

from functions import (
    get_hierarchical_dict_second,
    get_price_in_number,
    recursion_dict_extend_dict,
    filter_list
)

from core import ALLOWED_MARKS

texnomart_categories = {
    'smartphone': {
        'category': 'katalog',
        'sub_category': 'smartfony',
    }
}


class ParserTexnomart:
    def __init__(self, category, sub_category):
        self.URL = "https://texnomart.uz"
        self.category = category
        self.sub_category = sub_category

    async def get_soup(self, page=None):
        url = f"{self.URL}/ru/{self.category}/{self.sub_category}/"

        if page is not None:
            url += f"?page={page}"

        print('\n')
        print(f'URL: {url}')
        print('\n')

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print("Status Code: " + str(response.status))
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    return soup
                raise Exception("Status Code: " + str(response.status))

    async def get_json_data(self):
        json_data = dict()
        total_page = await self.get_pagination_number()
        if not total_page:
            raise Exception("Pagination number must be an integer")

        tasks = [self.get_page_data(page_number) for page_number in range(1, total_page + 1)]
        page_data = await asyncio.gather(*tasks)

        await asyncio.gather(*[recursion_dict_extend_dict(json_data, data) for data in page_data])
        return json_data

    async def get_page_data(self, page_number: int):
        page_data: dict = {}
        soup = await self.get_soup(page_number)

        cards = soup.find_all("div", class_="product-item-wrapper")

        for card in cards:

            link = self.URL + card.find("a", class_="product-name")['href']
            title = card.find("a", class_="product-name").get_text(strip=True)
            price = get_price_in_number(card.find("div", class_="product-price__current").get_text(strip=True))
            price_credit = get_price_in_number(card.find("div", class_="installment-price").get_text(strip=True))

            if title.lower().split(" ")[1] in ALLOWED_MARKS:
                data = {
                    "link": link,
                    "title": title,
                    "price": price,
                    "price_credit": price_credit // 100,
                }
            else:
                continue

            items = title.lower().split(" ")
            filter_list(items)
            get_hierarchical_dict_second(page_data, items[1:], data)

        return page_data

    async def get_pagination_number(self):
        soup = await self.get_soup()
        pagination = soup.select(
            "#catalog__page > div.catalog-content__products > div:nth-child(2) > div.pagination > div > div.vue-ads-flex-grow.vue-ads-flex.vue-ads-justify-end > button:nth-child(8)")
        number = pagination[0].get_text(strip=True)

        return int(number)

    async def write_json_file(self):
        json_data = await self.get_json_data()
        os.makedirs('json_data', exist_ok=True)
        with open('json_data/texnomart.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    async def run(self):
        await self.write_json_file()


parser = ParserTexnomart(
    category=texnomart_categories['smartphone']['category'],
    sub_category=texnomart_categories['smartphone']['sub_category']
)

if __name__ == "__main__":
    pass
    # asyncio.run(parser.get_page_data(1))
    start_time = time.perf_counter()
    while True:
        print('Start parsing!...')
        try:
            asyncio.run(parser.run())
            break
        except Exception as e:
            end_time = time.perf_counter()
            total_time = round(end_time - start_time, 3)
            print('Total time: ' + str(total_time))
            print(e)
            print('Parsing is sleeping!...')
            time.sleep(5)
            start_time = time.perf_counter()
    end_time = time.perf_counter()
    total_time = round(end_time - start_time, 3)
    print('Total time: ' + str(total_time))
