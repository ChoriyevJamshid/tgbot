from asgiref.sync import sync_to_async
from aiogram import Bot, types, Router, F
from aiogram.filters import CommandStart, Command
from keyboards.inline import get_keyboard, json_data
from funtions.orm import get_product_from_db

private_router = Router()

users_data = dict()


@private_router.message(CommandStart())
async def command_start(message: types.Message):
    chat_id = message.chat.id
    users_data[str(chat_id)] = dict()
    print(users_data)

    text = """
Assalomu alaykum!    
Quydagi tugmalardan birini tanlang
"""
    return await message.answer(
        text,
        reply_markup=get_keyboard([])
    )


@private_router.callback_query(F.data.startswith('value_'))
async def get_button_callback(callback: types.CallbackQuery):

    print(f'\n{callback.data}\n')
    chat_id = callback.message.chat.id

    data: dict = users_data.get(str(chat_id))

    if data is None:
        data = users_data[f'{chat_id}'] = dict()

    values = data.get('values')

    if values is None:
        values = data['values'] = list()

    _, value = callback.data.split('_')
    message_id = callback.message.message_id
    values.append(value)

    button_texts = json_data
    for value in values:
        if button_texts.get(value):
            button_texts = button_texts[value]
        else:
            button_texts = {}

    text = data.get('text', '')
    text += f"{value.title()} "

    data['text'] = text
    data['values'] = values
    users_data[str(chat_id)] = data

    if len(tuple(button_texts.keys())) == 0:
        return await return_data(callback.message)

    await callback.message.edit_text(text, reply_markup=get_keyboard(values, sizes=(4,)))
    await callback.answer()


async def return_data(message: types.Message):
    chat_id = message.chat.id
    data = users_data[str(chat_id)]
    values = data['values']

    product = await sync_to_async(get_product_from_db)(values)
    text = f"Your question: {users_data[str(chat_id)]['text']}"
    await message.edit_text(text)
    if product:
        await message.answer(product.link)
        return await message.answer(f"""
Title: {product.title}
Price: {product.price} sum.
""")
    return await message.answer("Not Found")







