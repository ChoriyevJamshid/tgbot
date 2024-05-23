from asgiref.sync import sync_to_async
from aiogram import Bot, types, Router, F
from aiogram.filters import CommandStart, Command
from keyboards.inline import get_keyboard, json_data, language_keyboard, generate_keyboard
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

    user, created = orm.get_or_create_user(session, chat_id, first_name, username)
    language = user.language if user.language else 'uz'
    text = texts_data[str(language)]

    if created:
        text = text['choose_language']['message']
        return await message.answer(
            text,
            reply_markup=language_keyboard()
        )

    return await get_start_text(message, user, bot)


@users_private_router.message(Command('lang'))
async def change_language(message: types.Message, session, bot: Bot):
    chat_id = message.chat.id
    message_id = message.message_id
    user, created = orm.get_or_create_user(session, chat_id)
    language = user.language

    text = f"<b>{texts_data[language]['change_language']['message']}</b>"
    try:
        await bot.delete_message(chat_id, message_id)
        await bot.edit_message_text(
            text=text, chat_id=chat_id,
            message_id=message_id - 1,
            reply_markup=language_keyboard()
        )
    except Exception:
        await message.answer(text, reply_markup=language_keyboard())


@users_private_router.callback_query(F.data.startswith('other_'))
async def other_callbacks(callback: types.CallbackQuery, session, bot: Bot):
    chat_id = callback.message.chat.id
    user, created = orm.get_or_create_user(session, chat_id)
    language = user.language

    _, data = callback.data.split('_')

    if data == "search":
        text = f"<b>{texts_data[language]['choose']['message']}</b>"
        await callback.message.edit_text(text, reply_markup=get_keyboard([]))
    await callback.answer()


@users_private_router.callback_query(F.data.startswith('lang_'))
async def choose_language(callback: types.CallbackQuery, session, bot: Bot):
    chat_id = callback.message.chat.id
    user, created = orm.get_or_create_user(session, chat_id)

    _, language = callback.data.split('_')

    user.language = language
    user.save()

    text = f"<b><i>{texts_data[language]['choose_language']['message']}</i></b>"

    await callback.message.edit_text(text, reply_markup=get_keyboard([]))
    await callback.answer()


@users_private_router.callback_query(F.data.startswith('value_'))
async def choose_product(callback: types.CallbackQuery, session, bot: Bot):
    is_back = False
    removed = None
    chat_id = callback.message.chat.id

    user, created = orm.get_or_create_user(session, chat_id)
    language = user.language

    if user.current_values.get('values') is None:
        user.current_values['values'] = list()

    values: list = user.current_values['values']
    _, value = callback.data.split('_')

    if value == "back":
        if not values:
            return await get_start_text(callback.message, user, bot)
        else:
            removed = values.pop()
            is_back = True
    else:
        values.append(value)

    button_texts = json_data
    for value in values:
        if button_texts.get(value):
            button_texts = button_texts[value]
        else:
            button_texts = {}

    if not is_back:
        user.current_text += value.title() + " "
    else:
        user.current_text = user.current_text.replace(removed.title() + " ", "")
    user.current_values['values'] = values

    if not user.current_text:
        sizes = (2,)
        text = f"<b>{texts_data[language]['choose']['message']}</b>"
    else:
        sizes = (4,)
        text = f"<b><i>{user.current_text}</i></b>"

    if len(tuple(button_texts.keys())) == 0:
        await callback.answer()
        return await return_data(callback.message, session, bot)

    await callback.message.edit_text(text, reply_markup=get_keyboard(values, sizes=sizes))
    await callback.answer()


async def get_start_text(message, user, bot):
    language = user.language

    get_start_text_dict = texts_data[language]['start']
    text = ""
    text += f"🤖 <b>{get_start_text_dict['message']['line1']}</b>"
    text += f"\n<b><i>{get_start_text_dict['message']['line2']}</i></b>\n"
    text += f"<i>{get_start_text_dict['message']['line3']}</i>"
    text += f"<i>{get_start_text_dict['message']['line4']}</i>"
    text += f"<i>{get_start_text_dict['message']['line5']}</i>"
    await bot.delete_message(user.chat_id, message.message_id)
    return message.answer(text, reply_markup=generate_keyboard(
        {
            get_start_text_dict['button']['text']: "search"
        },
        sizes=(1,),
        value="other"
    ))


async def return_data(message: types.Message, session, bot: Bot):
    chat_id = message.chat.id
    user, created = orm.get_or_create_user(session, chat_id)

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

    get_start_text_dict = texts_data[language]['start']
    return message.answer(text, reply_markup=generate_keyboard(
        {
            get_start_text_dict['button']['text']: "search"
        },
        sizes=(1,),
        value="other"
    ))

