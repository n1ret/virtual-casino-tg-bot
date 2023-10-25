from aiogram import types
from aiogram.types import (
    InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button
)

from datetime import datetime, timedelta

from sql import DataBase
from utils import get_menu
from games import bj_process
from config import settings
from states import (
    BJStates
)


async def menu_cb(callback: types.CallbackQuery, db: DataBase, state):
    await callback.answer()
    await state.finish()

    tg_user = callback.from_user

    text, markup = await get_menu(db, tg_user)

    await callback.message.edit_text(text, reply_markup=markup)


async def daily_reward(callback: types.CallbackQuery, db: DataBase):
    await callback.answer()

    tg_user = callback.from_user

    user = await db.get_user(tg_user.id)

    now = datetime.now()

    if now >= user.reward_datetime:
        await db.add_money(tg_user.id, settings.DAILY_REWARD_AMOUNT)
        await db.set_reward_datetime(
            tg_user.id, now+timedelta(days=1)
        )
        text = f"Вы получили {settings.DAILY_REWARD_AMOUNT} монет"
    else:
        wait_for_reward = str(user.reward_datetime-now).split('.')[0]
        text = (
            "Ээээ, пидор, хули лезешь.\n"
            f"Ты уже получил сегодня свои монеты, возвращайся через {wait_for_reward}"
        )

    markup = Markup().add(
        Button("Menu", callback_data=f"menu:{tg_user.id}")
    )

    await callback.message.edit_text(
        text, reply_markup=markup
    )


async def casino(callback: types.CallbackQuery):
    await callback.answer()

    tg_user = callback.from_user

    text = "Игры"
    markup = Markup().add(
        Button("BJ", callback_data=f"bj_choice:{tg_user.id}")
    ).add(
        Button("Menu", callback_data=f"menu:{tg_user.id}")
    )

    await callback.message.edit_text(
        text, reply_markup=markup
    )


async def bj_choice(callback: types.CallbackQuery):
    await callback.answer()

    tg_user = callback.from_user

    await BJStates.username.set()

    text = "Введите @username оппонента"
    markup = Markup().add(
        Button("Menu", callback_data=f"menu:{tg_user.id}")
    )

    await callback.message.edit_text(
        text, reply_markup=markup
    )


async def bj_accept(callback: types.CallbackQuery):
    await callback.answer()

    tg_user = callback.from_user
    data = callback.data.split(':')
    first_user_id = data[2]

    first_user = (await callback.message.chat.get_member(first_user_id)).user

    await bj_process(callback.message, first_user, tg_user)


async def bj_deny(callback: types.CallbackQuery):
    await callback.answer()

    tg_user = callback.from_user

    text = f"@{tg_user.username} отказал"

    await callback.message.edit_text(
        text, reply_markup=Markup()
    )


async def bj_cancel(callback: types.CallbackQuery):
    await callback.answer()

    text = "Игра отменена"

    await callback.message.edit_text(
        text, reply_markup=Markup()
    )
