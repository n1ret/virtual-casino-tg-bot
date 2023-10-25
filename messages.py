from aiogram import types
from aiogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from aiogram.dispatcher import FSMContext

from utils import get_menu
from sql import DataBase


async def state(message: types.Message, state: FSMContext):
    await message.answer(f'{await state.get_state()} {await state.get_data()}')


async def menu(message: types.Message, db: DataBase, state: FSMContext):
    await state.finish()

    tg_user = message.from_user

    text, markup = await get_menu(db, tg_user)

    await message.answer(text, reply_markup=markup)


async def username_choice(message: types.Message, state: FSMContext):
    tg_user = message.from_user

    markup = Markup().add(
        Button("Menu", callback_data=f"menu:{tg_user.id}")
    )
    if not message.text.startswith("@") or ' ' in message.text:
        await message.answer(
            "Это не имя формата @username",
            reply_markup=markup
        )
        return
    if message.text.lstrip('@') == tg_user.username:
        await message.answer("Нельзя выбрать себя", reply_markup=markup)
        return

    await state.finish()

    text = f"{message.text} приглашён в BlackJack"
    markup = Markup().add(
        Button("Принять", callback_data=f"bj_accept:{message.text}:{tg_user.id}"),
        Button("Отказ", callback_data=f"bj_deny:{message.text}")
    ).add(
        Button("Отмена вызова", callback_data=f"bj_cancel:{tg_user.id}")
    )

    await message.answer(text, reply_markup=markup)


async def bj_bet(message: types.Message, db: DataBase, state: FSMContext):
    tg_user = message.from_user

    try:
        bet = int(message.text)
    except ValueError:
        await message.answer("Введите <b>целое число</b>")
        return
    
    if bet <= 0:
        await message.answer("Число должно быть <b>положительным</b>")
        return
    
    if bet > (await db.get_or_create_user(tg_user.id)).money:
        await message.answer("Ставка не может <b>превышать</b> твой <b>баланс</b>")
        return
    
    async with state.proxy() as data:
        data['bet'] = bet

    text = f"@{tg_user.username} поставил {bet}"

    await message.answer(text)
