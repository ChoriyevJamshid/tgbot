def get_hierarchical_dict(current_data: dict, items: list | tuple, data: dict) -> None:
    current_dict = current_data
    for index, item in enumerate(items):
        if current_dict.get(item) is None:
            if index == len(items) - 1:
                current_dict[item] = data
            else:
                current_dict[item] = {}
        current_dict = current_dict[item]


def get_hierarchical_dict_second(current_data: dict, items: list | tuple, data: dict) -> None:
    items = tuple(items)
    current_dict = current_data

    for index, item in enumerate(items):
        if current_dict.get(item) is None:
            if '/' in item or check_item(item):
                current_dict[item] = data
            else:
                current_dict[item] = {}
        current_dict = current_dict[item]
        if '/' in item or check_item(item):
            return


def get_hierarchical_dict_olcha(current_data: dict, items: list | tuple, data: dict) -> None:
    items = tuple(items)
    current_dict = current_data

    for index, item in enumerate(items):
        if current_dict.get(item) is None:
            if '/' in item or index == len(items) - 1:
                current_dict[item] = data
            else:
                current_dict[item] = {}
        current_dict = current_dict[item]
        if '/' in item:
            return


def is_pow_number(number: int, degree: int):
    if isinstance(number, int):
        while number > 1:
            number /= degree
        if number == 1:
            return True
    return False


def check_item(item):
    if item.isalnum() and is_pow_number(get_numbers_of_memory(item), 2):
        return True
    return False


def get_price_in_number(price: str):
    result = str()
    for letter in price:
        if letter.isdigit():
            result += letter
    if result.isdigit():
        return int(result)


def get_numbers_of_memory(text: str):
    condition, is_tb = check_memory_type_in_text(text)
    if condition:
        result = str()
        for letter in text:
            if letter.isdigit():
                result += letter
        if result.isdigit():
            if is_tb:
                return int(result) * 1024
            return int(result)


def check_memory_type_in_text(value: str):
    is_tb = False
    if 'гб' in value or 'gb' in value:
        return True, is_tb
    elif 'тб' in value or 'tb' in value or 'tб' in value:
        return True, not is_tb
    return False, is_tb


async def recursion_dict_extend_dict(main: dict, second: dict) -> None:
    for key, value in second.items():
        if key not in main.keys():
            main[key] = value
        else:
            if isinstance(main[key], dict):
                await recursion_dict_extend_dict(main[key], value)


def check_memory_type(value: str):
    if (value == 'гб' or value == 'гб,' or value == ',' \
        or value == 'gb') or \
            value == 'тб' or value == 'тб,' or value == ',' \
            or value == 'tb' or value == 'tб':
        return True
    return False


def filter_list(items: list) -> None:
    i = 0

    while i < len(items):
        join_item = str()

        if "\xa0a" in items[i]:
            val1, val2 = items[i].split("\xa0a")
            items[i] = val1
            items.insert(i + 1, val2)
            continue

        if check_memory_type(items[i]):
            del items[i]
        elif items[i] == "+":
            del items[i]
        else:
            i += 1

        if i + 2 < len(items):
            if "e-sim" in items[i] and "/" == items[i + 1] and "nano-sim" in items[i + 2]:
                join_item = f"{items[i]} {items[i + 1]} {items[i + 2]}"
                del items[i]
                del items[i]
                del items[i]
                items.insert(i, join_item)

        if i + 1 < len(items):
            if "только" in items[i] and "e-sim" in items[i + 1]:
                join_item = f"{items[i]} {items[i + 1]}"
                del items[i]
                del items[i]
                items.insert(i, join_item)


def filter_list_second(items: list) -> None:
    i = 0

    while i < len(items):
        join_item = str()

        if check_memory_type(items[i]):
            del items[i]
        elif items[i] == "+":
            del items[i]
        else:
            i += 1

        if i + 2 < len(items):
            if "e-sim" in items[i] and "/" == items[i + 1] and "nano-sim" in items[i + 2]:
                join_item = f"{items[i]} {items[i + 1]} {items[i + 2]}"
                del items[i]
                del items[i]
                del items[i]
                items.insert(i, join_item)

        if i + 1 < len(items):
            if "только" in items[i] and "e-sim" in items[i + 1]:
                join_item = f"{items[i]} {items[i + 1]}"
                del items[i]
                del items[i]
                items.insert(i, join_item)
