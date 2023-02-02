from aiogram import types


async def menu(message: types.Message, db):
    username = ""
    tg_user = message.from_user
    if tg_user:
        username = tg_user.username or tg_user.first_name

    user = await db.get_or_create_user(tg_user.id)

    markup = Markup().add(
        Button('Ежедневная награда', callback_data=f'daily_reward:{tg_user.id}')
    )
    await message.answer(f'Menu {username}', reply_markup=markup)


async def pussy(message: types.Message, db):
    print(db)
    await message.answer('Пизда')

