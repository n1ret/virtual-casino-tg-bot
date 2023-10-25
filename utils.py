from aiogram.types import (
    InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button,
    User
)
from aiogram import Dispatcher

from typing import Union

from sql import DataBase


async def get_menu(db: DataBase, tg_user: User) -> tuple[str, Markup]:
    username = ''
    if tg_user:
        username = tg_user.username or tg_user.first_name

    user = await db.get_or_create_user(tg_user.id)

    markup = Markup().add(
        Button('Казино', callback_data=f'casino:{tg_user.id}')
    ).add(
        Button('Ежедневная награда', callback_data=f'daily_reward:{tg_user.id}')
    )

    text = f'Menu {username}\nМонеты: {user.money}'

    return text, markup


def get_state(chat: Union[str, int, None] = None,
              user: Union[str, int, None] = None):
    state = Dispatcher.get_current().current_state(chat=chat, user=user)
    return state


async def finish_state(chat: Union[str, int, None] = None,
                       user: Union[str, int, None] = None):
    state = Dispatcher.get_current().current_state(chat=chat, user=user)
    await state.finish()
