from asgiref.sync import sync_to_async
from aiogram import Bot, types, Router, F
from aiogram.filters import CommandStart, Command
from keyboards.inline import get_keyboard, json_data, language_keyboard
from database.orm import data_dict
from database import orm
from langs.functions import save_to_database

save_to_database(data_dict)

users_private_router = Router()
texts_data = data_dict.texts_data


@users_private_router.message(CommandStart())
async def command_start(message: types.Message, session, bot: Bot):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    username = message.chat.username

    user = orm.get_or_create_user(session, chat_id, first_name, username)
    language = user.language
    text = f"{texts_data[str(language)]['start']['message']}"
    if not language:
        return await message.answer(
            text,
            reply_markup=language_keyboard()
        )
    return await message.answer(text, reply_markup=get_keyboard([]))


@users_private_router.message(Command('lang'))
async def change_language(message: types.Message, session, bot: Bot):
    chat_id = message.chat.id
    message_id = message.message_id - 1
    user = orm.get_or_create_user(session, chat_id)
    language = user.language

    text = f"<b>{texts_data[language]['change_language']['message']}</b>"
    try:
        await bot.edit_message_text(
            text=text, chat_id=chat_id,
            message_id=message_id,
            reply_markup=language_keyboard()
        )
        await bot.delete_message(chat_id, message_id)
    except Exception:
        await message.answer(text, reply_markup=language_keyboard())


@users_private_router.callback_query(F.data.startswith('lang_'))
async def choose_language(callback: types.CallbackQuery, session, bot: Bot):
    chat_id = callback.message.chat.id
    user = orm.get_or_create_user(session, chat_id)

    _, language = callback.data.split('_')

    user.language = language
    user.save()

    text = f"<b><i>{texts_data[language]['choose_language']['message']}</i></b>"

    await callback.message.edit_text(text, reply_markup=get_keyboard([]))
    await callback.answer()


@users_private_router.callback_query(F.data.startswith('value_'))
async def choose_product(callback: types.CallbackQuery, session, bot: Bot):
    chat_id = callback.message.chat.id

    user = orm.get_or_create_user(session, chat_id)

    if user.current_values.get('values') is None:
        user.current_values['values'] = list()

    values: list = user.current_values['values']
    _, value = callback.data.split('_')

    values.append(value)

    button_texts = json_data
    for value in values:
        if button_texts.get(value):
            button_texts = button_texts[value]
        else:
            button_texts = {}

    user.current_text += value.title() + " "
    user.current_values['values'] = values

    text = f"<b><i>{user.current_text}</i></b>"

    if len(tuple(button_texts.keys())) == 0:
        await callback.answer()
        return await return_data(callback.message, session, bot)

    await callback.message.edit_text(text, reply_markup=get_keyboard(values, sizes=(4,)))
    await callback.answer()


async def return_data(message: types.Message, session, bot: Bot):
    chat_id = message.chat.id
    user = orm.get_or_create_user(session, chat_id)

    language = user.language
    current_values = user.current_values['values']
    current_text = user.current_text

    orm.save_user_history(user, current_text, current_values)

    user.current_text = ''
    user.current_values['values'] = []
    user.save()

    products = await sync_to_async(orm.get_product_from_db)(current_values)
    product_data = None
    for data in products:
        if product_data is None:
            product_data = data
        else:
            if product_data['price'] > data['price']:
                product_data = data

    if products:
        txt = texts_data[language]['return_data']['message']
        text = f"<b>{txt}</b> <i>{current_text}</i>"
        await message.edit_text(text)

        for data in products:
            text = f"""
<b>Shop:</b> <i>{data['shop']}</i>
<b>Product:</b> <i>{data['product'].title.title()}</i>
<b>Price:</b> <i>{data['price']}</i>
<b>Link:</b> <i>{data['product'].link}</i>
"""
            await message.answer(text)
        txt = texts_data[language]['return_data']['message2']
        text = f'''
<b>{txt}:</b> <i>{current_text.title()}</i>
<i>{product_data['product'].link}</i>
        '''
    else:
        txt = texts_data[language]['return_data']['message3']
        text = f"<h2>{txt}</h2>"
    return await message.answer(text)

# version1

# @users_private_router.message(CommandStart())
# async def command_start(message: types.Message):
#     chat_id = message.chat.id
#
#     if users_data.get(str(chat_id), None) is None:
#         users_data[str(chat_id)] = dict()
#     user_data = users_data[str(chat_id)]
#
#     if user_data.get('language', None) is None:
#         user_data['language'] = 'uz'
#
#     text = texts_data[user_data['language']]['start']['message']
#     save_users_data(users_data, chat_id, user_data)
#
#     return await message.answer(
#         text,
#         reply_markup=language_keyboard()
#     )
#
#
# @users_private_router.callback_query(F.data.startswith('value_'))
# async def choose_product(callback: types.CallbackQuery):
#
#     print(f'\n{callback.data}\n')
#     chat_id = callback.message.chat.id
#
#     user_data = users_data[str(chat_id)]
#
#     if user_data.get('current_values') is None:
#         user_data['current_values'] = list()
#
#     current_values = user_data['current_values']
#
#     _, value = callback.data.split('_')
#     current_values.append(value)
#
#     button_texts = json_data
#     for value in current_values:
#         if button_texts.get(value):
#             button_texts = button_texts[value]
#         else:
#             button_texts = {}
#     if user_data.get('current_text', None) is None:
#         user_data['current_text'] = ''
#     text = user_data['current_text']
#     text += f"{value.title()} "
#
#     user_data['current_text'] = text
#     user_data['current_values'] = current_values
#     save_users_data(users_data, chat_id, user_data)
#
#     if len(tuple(button_texts.keys())) == 0:
#         await callback.answer()
#         return await return_data(callback.message)
#
#     await callback.message.edit_text(text, reply_markup=get_keyboard(current_values, sizes=(4,)))
#     await callback.answer()
#
# @users_private_router.callback_query(F.data.startswith('lang_'))
# async def choose_language(callback: types.CallbackQuery):
#
#     chat_id = callback.message.chat.id
#     user_data = users_data[str(chat_id)]
#
#     _, language = callback.data.split('_')
#
#     user_data['language'] = language
#     users_data[str(chat_id)] = user_data
#     save_users_data(users_data, chat_id, user_data)
#
#     text = texts_data[user_data['language']]['choose_language']['message']
#
#     await callback.message.edit_text(text, reply_markup=get_keyboard([]))
#     await callback.answer()
#
#
# async def return_data(message: types.Message):
#     chat_id = message.chat.id
#     user_data = users_data[str(chat_id)]
#     current_values = user_data['current_values']
#     current_text = user_data['current_text']
#
#     if user_data.get('history') is None:
#         user_data['history'] = dict()
#         user_data['history']['texts'] = list()
#         user_data['history']['values'] = list()
#     user_data['history']['texts'].append(current_text)
#     user_data['history']['values'].append(current_values)
#
#     user_data['current_text'] = ''
#     user_data['current_values'] = []
#     save_users_data(users_data, chat_id, user_data)
#
#     products = await sync_to_async(get_product_from_db)(current_values)
#     product_data = None
#     for data in products:
#         if product_data is None:
#             product_data = data
#         else:
#             if product_data['price'] > data['price']:
#                 product_data = data
#
#     txt = texts_data[user_data['language']]['return_data']['message']
#     text = f"{txt} {current_text}"
#     await message.edit_text(text)
#
#     for data in products:
#         text = f"""
# Shop: {data['shop']}
# Product: {data['product'].title.title()}
# Price: {data['price']}
# Link: {data['product'].link}
# """
#         await message.answer(text)
#     txt = texts_data[user_data['language']]['return_data']['message2']
#     text = f'''
# {txt}: {current_text.title()}
# {product_data['product'].link}
#     '''
#     return await message.answer(text)
