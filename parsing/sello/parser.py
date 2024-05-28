from parsing.base.parser import *

debug = False

categories = {
    'smartphone': {
        'category': 'telefony-i-smart-casy',
        'subcategory': 'smartfony',
    }
}
dir_name = str(os.path.dirname(__file__)).split('/')[-1]


class Parser(BaseParser):
    def __init__(self, category, subcategory, *args):
        super().__init__()
        self.URL = 'https://sello.uz'
        self.category = category
        self.subcategory = subcategory
        self.file = __file__
        self.function = append_dict
        self.dirname = args[0]
        self.category_type = args[1]

    async def get_soup(self, page=None):
        url = f"{self.URL}/category/elektronika/{self.category}/{self.subcategory}"

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

    async def get_page_data(self, page_number) -> dict:
        hierarchical_dict = dict()
        page_data: dict = {}
        soup = await self.get_soup(page_number)

        cards = soup.find_all('div', class_='col mb-3')
        i = 0
        for index, card in enumerate(cards):
            link = self.URL + card.find('a', class_="d-block p-1")['href']
            title = card.find("span", class_="t-truncate-4").get_text(strip=True)
            price = get_number_from_text(
                card.select(
                    f"#__next > div.w-100.h-100.mt-2.mt-lg-0.mb-3 > div.container.py-2 > div.d-block.d-md-flex > div:nth-child(2) > div.row.gx-2.gx-lg-3.row-cols-2.row-cols-sm-3.row-cols-md-4.row-cols-lg-5.row-cols-xl-5 > div:nth-child({index + 1}) > div > div.px-2.pb-3.position-relative > div")[
                    0].get_text(strip=True))

            item_list = title.lower().split(' ')[1:]

            if item_list[0] in ALLOWED_MARKS:
                data = {
                    'link': link,
                    'title': title,
                    'price': price,
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
        pagination = soup.find_all("li", class_="page-item")[-2]
        number = pagination.get_text(strip=True)
        if number:
            return int(number)
        return 0


def remove_bracket(letters):
    result = ''
    for letter in letters:
        if letter == '(' or letter == ')':
            continue
        result += letter
    return result

def filter_list(items: list) -> list:

    removing_items = [
        'gод', 'gаранtии', 'midnight', 'gолуbой', 'design', 'eu', 'forest', 'moonlight', 'aurora', 'mint',
        'ice', 'polar', 'sky', '+', 'sea', 'pebble', '2022', 'carbon', 'graphite', 'cyan', 'dark', '1', 'phantom',
        'emerald', 'sunrise', 'sm-a245', 'pink', 's916', 'light'
    ]

    result = items
    i = 0
    for i in range(len(items)):
        _break = False
        items[i] = convert_en(items[i])
        items[i] = remove_bracket(items[i])

        if ',' in items[i]:
            items[i] = items[i].replace(',', '')

        if 'gb' in items[i]:
            if items[i].isalpha():
                result = items[:i]
                break

            items[i] = items[i].replace('gb', '')
            _break = True

        if 'tb' in items[i]:
            if items[i].isalpha():
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
    result.pop(i - 1)
    if result[0] == 'samsung' and result[1] == 'galaxy':
        result.pop(1)

    if len(result) >= 5:
        result.pop(len(result) - 2)

    for item in removing_items:
        if item in result:
            result.remove(item)

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
    with open('json_data/kwargs_sello..json', mode='w', encoding='utf-8') as file:
        json.dump(parser.kwargs, file, indent=4, ensure_ascii=False)
else:
    pass





