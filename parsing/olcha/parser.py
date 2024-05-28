from ..base.parser import *

debug = False

categories = {
    'smartphone': {
        'category': 'telefony-gadzhety-aksessuary',
        'subcategory': 'telefony',
    }
}

dir_name = str(os.path.dirname(__file__)).split('/')[-1]


class Parser(BaseParser):
    def __init__(self, category, subcategory, *args):
        super().__init__()
        self.URL = "https://olcha.uz"
        self.category = category
        self.subcategory = subcategory
        self.function = append_dict
        self.dirname = args[0]
        self.category_type = args[1]

    async def get_soup(self, page=None):

        url = f"{self.URL}/ru/category/{self.category}/{self.subcategory}"

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
        cards = soup.find_all("div", class_="product-card")
        index = 0
        i = 0
        for index, card in enumerate(cards):
            link = self.URL + card.find("a", class_="product-card__link")['href']
            title = card.find("div", class_="product-card__brand-name").get_text(strip=True)
            price = get_number_from_text(card.find("div", class_="price__main").get_text(strip=True))
            price_credit = get_number_from_text(card.find("div", class_="price__credit").get_text(strip=True))

            item_list = title.lower().split(' ')

            if item_list[0] in ALLOWED_MARKS and price > 1_000_000:
                data = {
                    'link': link,
                    'title': title,
                    'price': price,
                    'price_credit': price_credit // 100
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
        pagination = soup.find("div", class_="paginations__wrapper")
        number = pagination.find_all("a", class_="paginations__item")[-2]
        if number:
            return int(number.get_text(strip=True))
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
        'черный', 'синий', 'black', 'sm-a045', 'кремовый', 'фиолеtовый', 'зеленый', 'india', 'midnight',
        'blue', 'желtый', 'свеtло-синий', 'china', 'white', "asia", 'version', 'серый', 'pebble',
        'white', 'gray', 'global', 'green', 'silver', 'перламуtровый', 'сереbрисtый', 'eu', 'bелый',
        'ice', "glacier", 'ocean', 'shimmering', 'deep', 'emerald', 'ge2ae', 'carbon', 'sea'
    ]

    result = items
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

        elif 'tb' in items[i]:
            if items[i].isalpha():
                result = items[:i]
                break

            items[i] = items[i].replace('tb', '')
            _break = True

        if "bывший" in items[i]:
            result = items[:i]
            break

        if '/' in items[i]:
            items[i] = remove_bracket(items[i])
            result = items[:i + 1]
            break

        if '(' in items[i] and '+' in items[i] and ')' in items[i]:
            items[i] = str(items[i]).replace('+', '/')

        if _break:
            result = items[:i + 1]
            break
    if result[0] == 'samsung' and result[1] == 'galaxy':
        result.pop(1)
    elif result[0] == 'galaxy':
        result[0] = 'samsung'

    for item in removing_items:
        if item in result:
            result.remove(item)
    while "" in result:
        result.remove("")

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


if __name__ == '__main__':
    parser = Parser(
        categories['smartphone']['category'],
        categories['smartphone']['subcategory'],
        *(dir_name, 'smarthphone')
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
    with open('json_data/kwargs_olcha..json', mode='w', encoding='utf-8') as file:
        json.dump(parser.kwargs, file, indent=4, ensure_ascii=False)
