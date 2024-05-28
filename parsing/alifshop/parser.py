# from parsing.base.parser import *
from parsing.base.parser import *

debug = False
categories = {
    'smartphone': {
        'category': 'categories',
        'subcategory': 'smartfoni-i-telefoni',
    }
}
dir_name = str(os.path.dirname(__file__)).split('/')[-1]


class Parser(BaseParser):
    def __init__(self, category, subcategory, *args):
        super().__init__()
        self.URL = 'https://alifshop.uz'
        self.category = category
        self.subcategory = subcategory
        self.function = append_dict
        self.dirname = args[0]
        self.category_type = args[1]

    async def get_soup(self, page=None):
        url = f"{self.URL}/ru/{self.category}/{self.subcategory}/"

        if page is not None:
            url += f"?page={page}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        html, status = await self.async_fetch(url=url, headers=headers)
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    async def get_page_data(self, page_number) -> dict:

        page_data: dict = {}
        hierarchical_dict = dict()

        soup = await self.get_soup(page_number)

        main = soup.find("main", class_="flex-grow")
        cards = main.find_all("div", class_="h-full grid grid-cols-1 content-between")
        index = 0
        i = 0
        for index, card in enumerate(cards):

            link = self.URL + card.find("a", class_="cursor-pointer")["href"]
            title = card.find("p", class_="max-w-xs text-sm text-grey-900 line-clamp-2 text-ellipsis mb-1").get_text(
                strip=True)

            price_credit = card.find("strong", class_="mr-0.5 font-medium").get_text(strip=True)
            price: list = card.select_one(
                f"#__nuxt > div > div.flex.flex-col.h-full > main > div.container.mb-6 > div.flex.flex-col.gap-6.md\:flex-row.relative.w-full > div.md\:basis-5\/6.mb-12.w-full > div.grid.grid-cols-2.md\:grid-cols-3.lg\:grid-cols-4.gap-5.mb-9 > div:nth-child({index + 1}) > a > figure > figcaption > div > p.text-red.text-sm")

            if not price:
                price: list = card.select_one(
                    f"#__nuxt > div > div.flex.flex-col.h-full > main > div.container.mb-6 > div.flex.flex-col.gap-6.md\:flex-row.relative.w-full > div.md\:basis-5\/6.mb-12.w-full > div.grid.grid-cols-2.md\:grid-cols-3.lg\:grid-cols-4.gap-5.mb-9 > div:nth-child({index + 1}) > a > figure > figcaption > p.text-grey-400.text-sm")
            price, _ = price.get_text(strip=True).split(' ')

            price = get_number_from_text(price)
            price_credit = get_number_from_text(price_credit)

            item_list = title.lower().split(" ")[1:]
            try:
                if item_list and item_list[0] in ALLOWED_MARKS:
                    data = {
                        'link': link,
                        'title': title,
                        'price': price,
                        'price_credit': price_credit,
                    }
                    i += 1
                else:
                    continue
            except Exception as e:
                continue
            item_list = filter_list(item_list)

            get_hierarchical_dict(hierarchical_dict, item_list, {})

            page_data[str(i)] = data
        print(f'\nPage number: {page_number}, append = {i} elements\n')
        await recursion_dict_extend_dict(self.kwargs, hierarchical_dict)
        return page_data

    async def get_total_page(self) -> int:
        soup = await self.get_soup()
        pagination = soup.find("nav", {"aria-label": "Pagination"}).get_text()
        number = pagination.split(' ')[-1]
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
        'sm-a135', ""
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

        elif '/' in items[i]:
            result = items[:i + 1]
            break

        if _break:
            result = items[:i + 1]
            break
    if result[0] == 'samsung':
        result.remove('galaxy')

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
elif __name__ == "__main__":
    pass
