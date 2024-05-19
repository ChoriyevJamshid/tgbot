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


from parsers import ALLOWED_MARKS


alif_shop_categories = {
    'smartphone': {
        'category': 'categories',
        'sub_category': 'smartfoni-i-telefoni',
    }
}


class ParserAlifShop:

    def __init__(self, category, sub_category):
        self.URL = "https://alifshop.uz"
        self.category = category
        self.sub_category = sub_category

    async def get_soup(self, page=None):
        url = f"{self.URL}/ru/{self.category}/{self.sub_category}/"

        if page is not None:
            url += f"?page={page}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # print("Status Code: " + str(response.status))
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    return soup
                raise Exception("Status Code: " + str(response.status))

    async def get_json_data(self):
        json_data = dict()
        total_page = await self.get_pagination_number()
        if not total_page.isdigit():
            raise Exception("Pagination number must be an integer")

        tasks = [self.get_page_data(page_number) for page_number in range(1, int(total_page) + 1)]
        page_data = await asyncio.gather(*tasks)

        await asyncio.gather(*[recursion_dict_extend_dict(json_data, data) for data in page_data])
        return json_data

    async def get_page_data(self, page_number: int):
        page_data: dict = {}
        soup = await self.get_soup(page_number)

        main = soup.find("main", class_="flex-grow")
        cards = main.find_all("div", class_="h-full grid grid-cols-1 content-between")

        for index, card in enumerate(cards):

            link = self.URL + card.find("a", class_="cursor-pointer")["href"]
            title = card.find("p", class_="max-w-xs text-sm text-grey-900 line-clamp-2 text-ellipsis mb-1").get_text(strip=True)

            price_credit = card.find("strong", class_="mr-0.5 font-medium").get_text(strip=True)
            price: list = card.select_one(
                f"#__nuxt > div > div.flex.flex-col.h-full > main > div.container.mb-6 > div.flex.flex-col.gap-6.md\:flex-row.relative.w-full > div.md\:basis-5\/6.mb-12.w-full > div.grid.grid-cols-2.md\:grid-cols-3.lg\:grid-cols-4.gap-5.mb-9 > div:nth-child({index + 1}) > a > figure > figcaption > div > p.text-red.text-sm")

            if not price:
                price = card.select_one(
                    f"#__nuxt > div > div.flex.flex-col.h-full > main > div.container.mb-6 > div.flex.flex-col.gap-6.md\:flex-row.relative.w-full > div.md\:basis-5\/6.mb-12.w-full > div.grid.grid-cols-2.md\:grid-cols-3.lg\:grid-cols-4.gap-5.mb-9 > div:nth-child({index + 1}) > a > figure > figcaption > p.text-grey-400.text-sm")
            price, _ = price.get_text(strip=True).split(' ')

            price = get_price_in_number(price)
            price_credit = get_price_in_number(price_credit)

            items = title.lower().split(" ")[1:]

            if items[0] in ALLOWED_MARKS:
                data = {
                    'link': link,
                    'title': title,
                    'price': price,
                    'price_credit': price_credit,
                }
            else:
                continue

            filter_list(items)
            get_hierarchical_dict_second(page_data, items, data)

        return page_data

    async def get_pagination_number(self):
        soup = await self.get_soup()
        pagination = soup.find("nav", {"aria-label": "Pagination"}).get_text()
        number = pagination.split(' ')[-1]
        return number

    async def write_json_file(self):
        json_data = await self.get_json_data()
        os.makedirs('json_data', exist_ok=True)
        with open('json_data/alifshop.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    async def run(self):
        await self.write_json_file()


parser = ParserAlifShop(
    category=alif_shop_categories['smartphone']['category'],
    sub_category=alif_shop_categories['smartphone']['sub_category']
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
