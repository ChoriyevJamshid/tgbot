from parsing.base.parser import *

debug = True

categories = {
    'smartphone': {
        'category': 'katalog',
        'subcategory': 'smartfony',
    }
}

dir_name = str(os.path.dirname(__file__)).split('/')[-1]


class Parser(BaseParser):
    def __init__(self, category, subcategory, *args):
        super().__init__()
        self.URL = "https://texnomart.uz"
        self.category = category
        self.subcategory = subcategory
        self.function = append_dict
        self.dirname = args[0]
        self.category_type = args[1]

    async def get_soup(self, page=None):
        url = f"{self.URL}/ru/{self.category}/{self.subcategory}/"

        # print(f'\n{url}\n')

        if page is not None:
            url += f"?page={page}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        html, status = await self.async_fetch(url=url, headers=headers)
        # print(f"\nStatus code: {status}\n")
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    async def get_page_data(self, page_number, i=0) -> dict:
        hierarchical_dict = dict()
        page_data: dict = {}
        soup = await self.get_soup(page_number)

        cards = soup.find_all("div", class_="product-item-wrapper")
        i = 0
        for index, card in enumerate(cards):

            link = self.URL + card.find("a", class_="product-name")['href']
            title = card.find("a", class_="product-name").get_text(strip=True)
            price = get_number_from_text(card.find("div", class_="product-price__current").get_text(strip=True))
            price_credit = get_number_from_text(card.find("div", class_="installment-price").get_text(strip=True))

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

            item_list = filter_list(item_list)
            get_hierarchical_dict(hierarchical_dict, item_list, {})

            page_data[str(i)] = data
        print(f'\nPage number: {page_number}, append = {i} elements\n')
        await recursion_dict_extend_dict(self.kwargs, hierarchical_dict)
        return page_data

    async def get_total_page(self) -> int:
        soup = await self.get_soup()
        pagination = soup.select(
            "#catalog__page > div.catalog-content__products > div:nth-child(2) > div.pagination > div > div.vue-ads-flex-grow.vue-ads-flex.vue-ads-justify-end > button:nth-child(8)")
        number = pagination[0].get_text(strip=True)
        if number:
            return int(number)
        return 0

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

    if result[0] == 'samsung' and result[1] == 'galaxy':
        result.pop(1)

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
    parser = Parser(
        categories['smartphone']['category'],
        categories['smartphone']['subcategory'],
        dir_name
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
