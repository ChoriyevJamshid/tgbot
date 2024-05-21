from parsing.base.parser import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--no-sandbox')
# options.add_argument("--headless")
options.add_argument('--disable-dev-shm-usage')
debug = False

categories = {
    'smartphone': {
        'category': 'category',
        'subcategory': 'smartfony-12690',
    }
}

dir_name = str(os.path.dirname(__file__)).split('/')[-1]


def recursion_dict_extend_dict(main: dict, second: dict) -> None:
    for key, value in second.items():
        if key not in main.keys():
            main[key] = value
        else:
            if isinstance(main[key], dict):
                recursion_dict_extend_dict(main[key], value)


def append_dict(main: dict, second: dict, key) -> None:
    main[key] = second


async def async_append_dict(main: dict, second: dict, key) -> None:
    main[key] = second


class Parser(BaseParser):

    def __init__(self, category, subcategory, dirname):
        super().__init__(dirname)

        self.category = category
        self.subcategory = subcategory

        self.URL = f'https://uzum.uz'
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

    def get_soup(self, page=None):
        browser = webdriver.Chrome()
        browser.get(self.URL + f"/{self.category}/{self.subcategory}")
        time.sleep(10)
        html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        return soup

    def get_json_data(self):

        json_data = dict()
        total_page = self.get_total_page()
        if not total_page:
            raise Exception("Pagination number must be an integer")

        for page_number in range(1, total_page + 1):
            page_data = self.get_page_data(page_number, total_page * (page_number - 1))
            append_dict(json_data, page_data, page_number)

        return json_data

    def get_page_data(self, page_number, i=0) -> dict:

        page_data = dict()
        soup = self.get_soup(page_number)
        cards_div = soup.find("div", id="category-products")

        cards = cards_div.find_all("div", class_="product-card")
        # print(cards)
        for card in cards:
            card_block = card.find("div", class_="card-info-block")

            link = self.URL + card_block.find("a", class_="subtitle-item")['href']
            title = card_block.find("a", class_="subtitle-item").get_text(strip=True)
            price_credit = get_number_from_text(card_block.find("div", class_="badge").get_text(strip=True))
            price = get_number_from_text(card.find("span", class_="product-card-price").get_text(strip=True))

            data = {
                'link': link,
                'title': title,
                'price': price,
                'price_credit': price_credit,
            }

            i += 1
            page_data[i] = data
        print(len(page_data))
        return page_data

    def get_total_page(self) -> int:
        soup = self.get_soup()
        return 27

    def write_json_file(self):
        json_data = self.get_json_data()
        os.makedirs('json_data', exist_ok=True)
        with open(f'json_data/{str(self.dirname)}.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    def run(self):
        self.write_json_file()


class AsyncParser:
    def __init__(self, category, subcategory, *args):
        self.category = category
        self.subcategory = subcategory
        self.dirname = args[0]
        self.category_type = args[1]
        self.exp_number = 0

        self.URL = f'https://uzum.uz'
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }


    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.HEADERS) as response:
                return await response.text()

    async def render_js_content(self, url, headers: dict):
        try:
            browser = await pyppeteer.launch()
            page = await browser.newPage()
            await page.setExtraHTTPHeaders(headers)
            await page.goto(url)
            await asyncio.sleep(15)
            # await page.waitFor(15000)
            content = await page.content()

            await browser.close()
            return content
        except Exception as e:
            print('-------------------------------\n')
            print(e)
            print('-------------------------------\n')
            await asyncio.sleep(5)
            await self.render_js_content(url, headers)

    async def get_soup(self, page=None):
        url = f"{self.URL}/uz/{self.category}/{self.subcategory}"

        if page is not None:
            url += f"?page={page}"

        browser = webdriver.Chrome(options=options)
        browser.get(self.URL + f"/{self.category}/{self.subcategory}")
        time.sleep(15)
        html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')
        print(soup)
        return soup

    async def get_json_data(self):
        json_data = dict()

        total_page = await self.get_total_page()
        if total_page == 0:
            raise Exception("Pagination number must be an integer")

        tasks = [self.get_page_data(i) for i in range(1, int(total_page) + 1)]
        page_data = await asyncio.gather(*tasks)

        await asyncio.gather(*[async_append_dict(json_data, data, index + 1) for index, data in enumerate(page_data)])
        return json_data

    async def get_page_data(self, page_number):
        page_data = dict()
        soup = await self.get_soup(page_number)
        i = 0
        try:
            cards_div = soup.find("div", id="category-products")

            cards = cards_div.find_all("div", class_="product-card")
            for index, card in enumerate(cards):
                card_block = card.find("div", class_="card-info-block")

                link = self.URL + card_block.find("a", class_="subtitle-item")['href']
                title = card_block.find("a", class_="subtitle-item").get_text(strip=True)
                price_credit = get_number_from_text(card_block.find("div", class_="badge").get_text(strip=True))
                price = get_number_from_text(card.find("span", class_="product-card-price").get_text(strip=True))

                item_list = title.lower().split(' ')[1:]

                if item_list[0] in ALLOWED_MARKS:
                    data = {
                        'link': link,
                        'title': title,
                        'price': price,
                        'price_credit': price_credit,
                    }
                    i += 1
                else:
                    continue
                print(item_list)
                page_data[str(i)] = data
        except Exception as e:
            print(f'\n{e}\n')
            await self.get_page_data(page_number)

        print(f'\nPage number: {page_number}, append = {i} elements\n')
        return page_data

    async def get_total_page(self) -> int:
        return 27

    async def write_json_file(self):
        json_data = await self.get_json_data()
        os.makedirs('json_data', exist_ok=True)
        # current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name = self.dirname + ".json"
        with open(f'json_data/{file_name}', 'w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    async def run(self):
        await self.write_json_file()

def filter_list(items: list) -> list:
    result = items
    for i in range(len(items)):
        _break = False
        items[i] = convert_en(items[i])

        if ',' in items[i]:
            items[i] = items[i].replace(',', '')

        if 'gb' in items[i]:
            if items[i].isalpha():
                result = items[:i]
                break

            items[i] = items[i].replace('gb', '')
            _break = True

        elif 'tb' in items[i]:
            if not str(items[i]).isalnum():
                result = items[:i]
                break

            items[i] = items[i].replace('gb', '')
            _break = True

        if '/' in items[i]:
            result = items[:i + 1]
            break

        if _break:
            result = items[:i + 1]
            break

    if result[0] == 'apple':
        result.pop(0)

    return result


def convert_en(letters: str):
    result = ""
    for letter in letters:
        if letter == "т":
            result += "t"
        elif letter == "б":
            result += "b"
        elif letter == "г":
            result += "g"
        else:
            result += letter
    return result

if __name__ == '__main__' and not debug:
    parser = AsyncParser(
        categories['smartphone']['category'],
        categories['smartphone']['subcategory'],
        *(dir_name, 'smartphone')
    )
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
else:
    pass

