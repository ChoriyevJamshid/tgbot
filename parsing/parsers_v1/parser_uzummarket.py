import os
import json
import time

import aiohttp
import asyncio
import pyppeteer
import httpx

from bs4 import BeautifulSoup, BeautifulStoneSoup
from pprint import pprint

from functions import (
    get_hierarchical_dict_second,
    get_price_in_number,
    recursion_dict_extend_dict,
    filter_list, get_hierarchical_dict
)

from parsers import ALLOWED_MARKS

uzum_market_categories = {
    'smartphone': {
        'category': 'category',
        'sub_category': 'smartfony-12690',
    }
}


class ParserUzumMarket:
    def __init__(self, category, sub_category):
        self.URL = "https://uzum.uz"
        self.category = category
        self.sub_category = sub_category

    async def fetch_page(self, url):
        async with aiohttp.ClientSession() as session:
            session.headers.add(
                key="User-Agent",
                value="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
            async with session.get(url) as response:
                return await response.text()

    async def render_with_js(self, url):
        browser = await pyppeteer.launch()
        page = await browser.newPage()
        await page.setExtraHTTPHeaders(headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        })
        await page.goto(url)
        await asyncio.sleep(30)
        content = await page.content()

        await browser.close()
        return content

    async def get_soup(self, page=None):
        url = f"{self.URL}/ru/{self.category}/{self.sub_category}"

        if page is not None:
            url += f"?currentPage={page}"

        rendered_html = await self.render_with_js(url)

        soup = BeautifulSoup(rendered_html, "html.parser")
        return soup

    async def get_json_data(self):
        json_data = dict()
        total_page = await self.get_pagination_number()
        if not total_page:
            raise Exception("Pagination number must be an integer")

        tasks = [self.get_page_data(page_number) for page_number in range(1, int(total_page) + 1)]
        page_data = await asyncio.gather(*tasks)

        await asyncio.gather(*[recursion_dict_extend_dict(json_data, data) for data in page_data])
        return json_data

    async def get_page_data(self, page_number: int):
        print('Page data_________________________________')
        page_data: dict = {}

        soup = await self.get_soup(page_number)
        cards_div = soup.find("div", id="category-products")

        cards = cards_div.find_all("div", class_="product-card")
        print(len(cards))
        print('\n')
        for card in cards:
            card_block = card.find("div", class_="card-info-block")

            link = self.URL + card_block.find("a", class_="subtitle-item")['href']
            title = card_block.find("a", class_="subtitle-item").get_text(strip=True)
            price_credit = get_price_in_number(card_block.find("div", class_="badge").get_text(strip=True))
            price = get_price_in_number(card.find("span", class_="product-card-price").get_text(strip=True))

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
            get_hierarchical_dict(page_data, items, data)

        pprint(page_data)

    async def get_pagination_number(self):
        soup = await self.get_soup()
        # pagination = soup.find("ul", class_="pagination desktop").get_text(strip=True)
        return 27

    async def write_json_file(self):
        json_data = await self.get_json_data()
        os.makedirs('json_data', exist_ok=True)
        with open('json_data/uzummarket.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    async def run(self):
        await self.write_json_file()


parser = ParserUzumMarket(
    category=uzum_market_categories['smartphone']['category'],
    sub_category=uzum_market_categories['smartphone']['sub_category']
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
