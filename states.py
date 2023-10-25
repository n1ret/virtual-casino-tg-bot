from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher

from typing import Union


class CustomState(State):
    async def set(self,
                  chat: Union[str, int, None] = None,
                  user: Union[str, int, None] = None):
        state = Dispatcher.get_current().current_state(chat=chat, user=user)
        await state.set_state(self.state)


class BJStates(StatesGroup):
    username = State()
    bet = CustomState()
