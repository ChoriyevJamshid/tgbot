import os
import json
import time
import selenium
import requests
import aiohttp
import asyncio
import pyppeteer
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
from pprint import pprint

ALLOWED_MARKS = ('apple', 'samsung', 'iphone', 'xiaomi', 'huawei',
                 'zte', 'vivo', 'oppo', 'honor', 'techno', 'infinix', 'oppo', 'realme', 'google')


def sync_recursion_dict_extend_dict(main: dict, second: dict, other=None) -> None:
    for key, value in second.items():
        if key not in main.keys():
            main[key] = value
        else:
            if isinstance(main[key], dict):
                sync_recursion_dict_extend_dict(main[key], value)


async def recursion_dict_extend_dict(main: dict, second: dict, other=None) -> None:
    for key, value in second.items():
        if key not in main.keys():
            main[key] = value
        else:
            if isinstance(main[key], dict):
                await recursion_dict_extend_dict(main[key], value)


async def append_dict(main: dict, second: dict, key) -> None:
    main[key] = second


def get_hierarchical_dict(current_data: dict, items: list | tuple, data: dict) -> None:
    current_dict = current_data
    for index, item in enumerate(items):
        if current_dict.get(item) is None:
            current_dict[item] = {}
        current_dict = current_dict[item]


def get_number_from_text(text: str) -> int:
    result = str()
    for letter in text:
        if letter.isdigit():
            result += letter
    if result.isdigit():
        return int(result)


class BaseParser:
    def __init__(self):
        self.function = append_dict
        self.file = __file__
        self.get_hierarchical_dict = None
        self.kwargs: dict = {}
        self.exp_number = 0
        self.dirname = None
        self.category_type = None

    def fetch(self, url, headers=None):
        response = requests.get(url)
        if headers is not None:
            response.headers.update(**headers)
        return response.text

    async def async_fetch(self, url, headers=None):
        async with aiohttp.ClientSession() as session:
            if headers:
                session.headers.extend(**headers)
            async with session.get(url) as response:
                return await response.text(), response.status

    async def get_json_data(self):
        json_data = dict()
        total_page: int = await self.get_total_page()

        if total_page == 0:
            raise Exception("Not found total page!")
        print(f'\nTotal pages: {total_page}\n')

        tasks = [self.get_page_data(page_number)
                 for page_number in range(1, total_page + 1)]
        page_data = await asyncio.gather(*tasks)

        await asyncio.gather(*[self.function(json_data, data, index + 1) for index, data in enumerate(page_data)])
        return json_data

    async def get_page_data(self, page_number) -> dict:
        pass

    async def get_total_page(self) -> int:
        return 0

    async def write_json_file(self):
        json_data = await self.get_json_data()

        os.makedirs('json_data', exist_ok=True)
        file_name = self.dirname + '.' + self.category_type + ".json"

        with open(f'json_data/{file_name}', mode='w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)


    async def run(self):
        await self.write_json_file()
