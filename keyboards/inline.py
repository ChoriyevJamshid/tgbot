import json
from pprint import pprint

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder

if __name__ == '__main__':
    path = '../json_data/kwargs.json'
else:
    path = 'json_data/kwargs.json'

with open(path, mode='r', encoding='utf-8') as json_file:
    json_data: dict = json.load(json_file)


def generate_keyboard(button_texts, sizes):

    keyboard = InlineKeyboardBuilder()
    # print(button_texts)
    for text in button_texts:
        keyboard.add(
            InlineKeyboardButton(
                text=f"📱 {str(text).title()}",
                callback_data=f"value_{str(text).lower()}")
        )
    return keyboard.adjust(*sizes).as_markup()




def get_keyboard(values: list, sizes=(2,)):

    if values:
        button_texts = json_data
        for index, value in enumerate(values):
            if button_texts.get(value):
                button_texts = button_texts[value]

            if len(list(button_texts.keys())) == 0:
                print('IS EMPTY')

        button_texts = list(button_texts.keys())
    else:
        button_texts = list(json_data.keys())
    return generate_keyboard(button_texts, sizes)


