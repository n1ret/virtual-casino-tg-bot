from aiogram import types


async def check_buttons_owner(callback: types.CallbackQuery):
    user_ids = callback.data.split(':')[1].split('|')
    if all([
        user_id != str(callback.from_user.id) and 
        user_id.lstrip('@') != callback.from_user.username
        for user_id in user_ids
    ]):
        await callback.answer('Положи на место чужие кнопки')
        return False
    return True


class CallbackFilter:
    def __init__(self, equal=None, startswith=None):
        if sum(not not i for i in (equal, startswith)) != 1:
            print("CallbackFilter WARN: must be one parameter")
        self.equal = equal
        self.startswith = startswith

    def __call__(self, cb):
        if self.equal and cb.data != self.equal:
            return False
        elif self.startswith and not cb.data.startswith(self.startswith):
            return False
        return True

