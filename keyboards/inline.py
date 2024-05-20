import json
from pprint import pprint
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.orm import data_dict

json_data = data_dict.json_data


def generate_keyboard(button_texts, sizes, value="value"):
    keyboard = InlineKeyboardBuilder()
    # print(button_texts)
    # if isinstance(button_texts, list):
    #     for text in button_texts:
    #         keyboard.add(
    #             InlineKeyboardButton(
    #                 text=f"{str(text).title()}",
    #                 callback_data=f"{value}_{str(text).lower()}")
    #         )
    # else:
    for text, cdata in button_texts.items():
        keyboard.add(
            InlineKeyboardButton(
                text=str(text.title()),
                callback_data=f"{value}_{cdata}"
            )
        )

    return keyboard.adjust(*sizes).as_markup()


def get_keyboard(values: list, sizes=(2,)):
    if values:
        button_texts = json_data
        for index, value in enumerate(values):
            if button_texts.get(value):
                button_texts = button_texts[value]
        button_texts = dict(zip(list(button_texts.keys()), list(button_texts.keys())))
    else:
        button_texts = dict(zip(list(json_data.keys()), list(json_data.keys())))
    return generate_keyboard(button_texts, sizes)


def language_keyboard():
    button_texts = {
        '🇺🇿 Uzbek': 'uz',
        '🇷🇺 Russian': 'ru',
        '🏴󠁧󠁢󠁥󠁮󠁧󠁿 English': 'en'
    }
    return generate_keyboard(button_texts, (1,), 'lang')


