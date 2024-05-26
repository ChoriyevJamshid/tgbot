def count_list_items(items):
    result_dict = {}
    for item in items:
        if not result_dict.get(item):
            result_dict[item] = 1
        else:
            result_dict[item] += 1
    return result_dict


numbers = "0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"


def get_pagination(total_page, page_number, page_slice=5):
    """
    Function: get_pagination()
    return: pagination dict
    """
    pagination = {}

    if total_page > 1:

        if page_number > 1:
            pagination['⬅️'] = 'previous'

        if total_page <= page_slice:
            for i in range(1, total_page + 1):
                if i == page_number:
                    number = numbers[page_number]
                    pagination[f"{number}"] = str(page_number)
                else:
                    pagination[str(i)] = str(i)

        else:
            for i in range(1, 3):
                if i == page_number:
                    number = numbers[page_number]
                    pagination[f"{number}"] = str(page_number)
                else:
                    pagination[str(i)] = str(i)

            if page_number > page_slice // 2 + 1:
                pagination["..."] = "..."

            if page_slice // 2 + 1 < page_number < total_page - 2:
                if page_number > 10:
                    in1 = page_number // 10
                    in2 = page_number % 10
                    number = numbers[in1] + numbers[in2]
                else:
                    number = numbers[page_number]
                pagination[f"{number}"] = str(page_number)

            if page_number < total_page - 2:
                pagination["..."] = "..."

            for i in range(total_page - 1, total_page + 1):
                if i == page_number:
                    if page_number > 10:
                        in1 = page_number // 10
                        in2 = page_number % 10
                        number = numbers[in1] + numbers[in2]
                    else:
                        number = numbers[page_number]
                    pagination[f"{number}"] = str(page_number)
                else:
                    pagination[str(i)] = str(i)

        if page_number < total_page:
            pagination['➡️'] = 'next'

    return pagination
