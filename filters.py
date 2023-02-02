from aiogram import types


async def check_user_button(callback: types.CallbackQuery):
    user_id = callback.data.split(':')[1]
    if user_id != callback.from_user.id:
        await callback.answer('Положи на место чужие кнопки')
        return False
    return True

