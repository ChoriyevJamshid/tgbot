from asgiref.sync import sync_to_async
from aiogram import Bot, types, Router, F
from aiogram.filters import Command
from database.orm import data_dict
from database import orm
from langs.functions import save_to_database
from keyboards.inline import generate_keyboard
from common.functions import count_list_items, get_pagination

save_to_database(data_dict)

admin_router = Router()
texts_data = data_dict.texts_data

markup = generate_keyboard(
    {
        'get users list': 'list',
        'get users number': 'number'
    },
    sizes=(1,),
    value='user'
)

PAGE = 1


@admin_router.message(Command('admin'))
async def admin_page(message: types.Message, session, bot: Bot):
    chat_id = message.chat.id
    user, created = orm.get_or_create_user(session, chat_id)

    if not user.is_admin:
        print(session)
        print(type(session))
        return await bot.delete_message(chat_id, message.message_id)

    text = texts_data[user.language]["choose"]["message"]
    return await message.answer(text, reply_markup=markup)


@admin_router.callback_query(F.data.startswith("user"))
async def get_users_info(callback: types.CallbackQuery, session, bot):
    chat_id = callback.message.chat.id
    user, created = orm.get_or_create_user(session, chat_id)
    lang = user.language

    _, value = callback.data.split("_")

    if value == "number":
        users_number = await sync_to_async(orm.get_users_number)()
        text = f"🤖 {texts_data[lang]['admin']['message']['number']}: {users_number}"
        await callback.message.edit_text(text, reply_markup=markup)

    elif value in ("list", 'back'):
        if session[str(chat_id)].get('users') is None:
            users = await sync_to_async(lambda: list(orm.get_users()))()
            session[str(chat_id)]['users'] = users

        if session[str(chat_id)].get('page_number') is None:
            session[str(chat_id)]['page_number'] = 1

        total_users = session[str(chat_id)]['users']
        total_page = int(len(total_users) / PAGE) + 1 if len(total_users) % PAGE else int(len(total_users) / PAGE)
        page_number = session[str(chat_id)]['page_number']

        if page_number == total_page:
            users = total_users[(page_number - 1) * PAGE:]
        elif page_number < total_page:
            users = total_users[(page_number - 1) * PAGE: page_number * PAGE]

        buttons_dict = {
            f"{i + 1} - {user.first_name}": f"{user.chat_id}" for i, user in enumerate(users)
        }

        pagination = get_pagination(total_page, page_number)

        buttons_dict['🔙'] = 'back'
        users_markup = generate_keyboard(
            buttons_dict,
            sizes=(1,),
            value="secret",
            **pagination
        )
        text = f"🤖 {texts_data[lang]['admin']['message']['list']} 📂"
        await callback.message.edit_text(text, reply_markup=users_markup)
    return await callback.answer()


@admin_router.callback_query(F.data.startswith('secret'))
async def get_user_info(callback: types.CallbackQuery, session, bot):
    chat_id = callback.message.chat.id
    user, created = orm.get_or_create_user(session, chat_id)
    lang = user.language

    total_users = session[str(chat_id)]['users']
    total_page = int(len(total_users) / PAGE) + 1 if len(total_users) % PAGE else int(len(total_users) / PAGE)

    _, value = callback.data.split('_')

    if value == "back":
        text = texts_data[user.language]["choose"]["message"]
        await callback.message.edit_text(text, reply_markup=markup)

    elif len(value) < 5 or value in ("next", "previous"):
        if value.isdigit():
            if int(value) == session[str(chat_id)]['page_number']:
                return callback.answer()
            session[str(chat_id)]['page_number'] = int(value)
        elif value == "next":
            session[str(chat_id)]['page_number'] += 1
        elif value == "previous":
            session[str(chat_id)]['page_number'] -= 1

        page_number = session[str(chat_id)]['page_number']

        if page_number == total_page:
            users = total_users[(page_number - 1) * PAGE:]
        elif page_number < total_page:
            users = total_users[(page_number - 1) * PAGE: page_number * PAGE]

        buttons_dict = {
            f"{i + 1} - {user.first_name}": f"{user.chat_id}" for i, user in enumerate(users)
        }

        pagination = get_pagination(total_page, page_number)

        buttons_dict['🔙'] = 'back'
        users_markup = generate_keyboard(
            buttons_dict,
            sizes=(1,),
            value="secret",
            **pagination
        )
        text = f"🤖 {texts_data[lang]['admin']['message']['list']} 📂"
        await callback.message.edit_text(text, reply_markup=users_markup)

    elif value == "next":
        session[str(chat_id)]['page_number'] += 1
    else:
        user, created = orm.get_or_create_user(session, int(value))
        history = await sync_to_async(orm.get_user_history)(user)
        texts = history.texts.get('texts', [])
        texts_dict = count_list_items(texts)

        text = ''

        for key, value in texts_dict.items():
            text += f"<b>{key}</b>:  <b><i>{value}</i></b>\n"

        await callback.message.edit_text(text, reply_markup=generate_keyboard(
            {
                '🔙': 'back'
            },
            sizes=(1,),
            value="user"
        ))

    return await callback.answer()
