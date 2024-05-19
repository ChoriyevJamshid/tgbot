import os
import json
import time

import aiohttp
import asyncio

import selenium
from bs4 import BeautifulSoup
from lxml import etree
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from functions import (
    get_hierarchical_dict_second,
    get_price_in_number,
    recursion_dict_extend_dict,
    filter_list,
    filter_list_second
)

from parsers import ALLOWED_MARKS

media_park_categories = {
    'smartphone': {
        'category': 'telefony-17',
        'sub_category': 'smartfony-40',
    }
}


class ParserMediaPark:
    def __init__(self, category, sub_category):
        self.URL = "https://mediapark.uz"
        self.category = category
        self.sub_category = sub_category
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Upgrade - Insecure - Requests': '1',
            'Service - Worker - Navigation - Preload': 'true',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uz;q=0.6',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd'

        }

    async def get_soup(self, page=None):
        url = f"{self.URL}/products/category/{self.category}/{self.sub_category}/"

        if page is not None:
            url += f"?page={page}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # print("Status Code: " + str(response.status))
                if response.status == 200:
                    html = await response.text()
                    # await asyncio.sleep(4)
                    soup = BeautifulSoup(html, "html.parser")
                    return soup
                raise Exception("Status Code: " + str(response.status))

    async def get_json_data(self):
        json_data = {}
        total_page = await self.get_pagination_number()
        if not total_page:
            raise Exception("Pagination number must be an integer")

        tasks = [self.get_page_data(page_number) for page_number in range(1, total_page + 1)]
        page_data = await asyncio.gather(*tasks)

        await asyncio.gather(*[recursion_dict_extend_dict(json_data, data) for data in page_data])
        return json_data

    async def get_page_data(self, page_number):
        page_data = {}
        soup = await self.get_soup(page_number)

        cards = soup.find_all("a", class_="product-cart")
        for card in cards:
            link = self.URL + card['href']
            title = card.find("p", class_="text-gray").get_text(strip=True)
            price = get_price_in_number(card.find("b", class_="text-dark").get_text(strip=True))
            price_credit = get_price_in_number(card.find("span", class_="text-blue-primary").get_text(strip=True))

            if True:
                data = {
                    'link': link,
                    'title': title,
                    'price': price,
                    'price_credit': price_credit,
                }
            else:
                continue

            items = title.lower().split(" ")

            filter_list(items)
            get_hierarchical_dict_second(page_data, items[1:], data)

        # pprint(page_data)
        return page_data

    async def get_pagination_number(self):

        soup = await self.get_soup(2)
        pagination = soup.find('ul', class_='pagination').get_text()
        return 20

    async def write_json_file(self):
        json_data = await self.get_json_data()
        os.makedirs('json_data', exist_ok=True)
        with open('json_data/mediapark.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    async def run(self):
        await self.write_json_file()


parser = ParserMediaPark(
    category=media_park_categories['smartphone']['category'],
    sub_category=media_park_categories['smartphone']['sub_category']
)


if __name__ == "__main__":
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
