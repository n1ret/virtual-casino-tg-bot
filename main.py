from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import filters
from aiogram.utils.exceptions import MessageToEditNotFound, MessageNotModified
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from os import environ
import logging
import asyncio

from sql import DataBase
from messages import (
    menu, username_choice, bj_bet, state
)
from callbacks import (
    menu_cb, daily_reward, casino, bj_choice, bj_accept, bj_deny, bj_cancel
)
from states import BJStates
from middlewares import DBMiddleware
from filters import check_buttons_owner, CallbackFilter
from errors import pass_error

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s[%(asctime)s] %(message)s')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
else:
    loop = asyncio.get_event_loop()

# Initialize database
db = DataBase(
    environ.get('PSQL_HOST'), environ.get('PSQL_DBNAME'),
    user=environ.get('PSQL_LOGIN'), password=environ.get('PSQL_PASSWORD'),
    loop=loop
)

if __name__ == '__main__':
    # Bot initialize
    bot = Bot(token=environ.get('TOKEN'), parse_mode="HTML")
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Registering middlewares
    dp.middleware.setup(DBMiddleware(db))

    # Messages handlers
    dp.register_message_handler(
        menu,
        filters.ChatTypeFilter('supergroup'), commands=['start', 'menu'],
        state='*'
    )
    dp.register_message_handler(
        state,
        filters.ChatTypeFilter('supergroup'), commands=['state'],
        state='*'
    )
    dp.register_message_handler(
        username_choice,
        filters.ChatTypeFilter('supergroup'), state=BJStates.username
    )
    dp.register_message_handler(
        bj_bet,
        filters.ChatTypeFilter('supergroup'), state=BJStates.bet
    )

    # Callbacks handlers
    dp.register_callback_query_handler(
        menu_cb, CallbackFilter(startswith='menu:'),
        check_buttons_owner, state='*'
    )
    dp.register_callback_query_handler(
        casino, CallbackFilter(startswith='casino:'), check_buttons_owner
    )
    dp.register_callback_query_handler(
        bj_choice, CallbackFilter(startswith='bj_choice:'), check_buttons_owner
    )
    dp.register_callback_query_handler(
        bj_accept, CallbackFilter(startswith='bj_accept:'), check_buttons_owner
    )
    dp.register_callback_query_handler(
        bj_deny, CallbackFilter(startswith='bj_deny:'), check_buttons_owner
    )
    dp.register_callback_query_handler(
        bj_cancel, CallbackFilter(startswith='bj_cancel:'), check_buttons_owner
    )
    dp.register_callback_query_handler(
        daily_reward, CallbackFilter(startswith='daily_reward:'),
        check_buttons_owner
    )

    # Errors handlers
    for error in (MessageToEditNotFound, MessageNotModified):
        dp.register_errors_handler(pass_error, exception=error)

    executor.start_polling(dp, skip_updates=True, loop=loop)
