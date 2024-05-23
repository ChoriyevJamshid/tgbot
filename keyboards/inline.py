import json
from pprint import pprint
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.orm import data_dict

json_data = data_dict.json_data


def generate_keyboard(button_texts, sizes, value="value"):
    keyboard = InlineKeyboardBuilder()
    for text, cdata in button_texts.items():
        keyboard.add(
            InlineKeyboardButton(
                text=str(text.title()),
                callback_data=f"{value}_{cdata}"
            )
        )

    keyboard = keyboard.adjust(*sizes)
    if value == "value":
        back_keyboard = InlineKeyboardBuilder()
        back_keyboard.add(
            InlineKeyboardButton(
                text="🔙",
                callback_data="value_back"
            )
        )
        keyboard.attach(back_keyboard)
    return keyboard.as_markup()


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


