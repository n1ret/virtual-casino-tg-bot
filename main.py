from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher import filters
from dotenv import load_dotenv

from os import environ
import logging
import asyncio

from sql import DataBase
from messages import (
    menu, pussy
)

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s[%(asctime)s] %(message)s')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
else:
    loop = asyncio.get_event_loop()
db = DataBase(
    environ.get('PSQL_HOST'), environ.get('PSQL_DBNAME'),
    user=environ.get('PSQL_LOGIN'), password=environ.get('PSQL_PASSWORD'),
    loop=loop
)

class DBMiddleware(BaseMiddleware):
    async def pre_process(
        self, obj, data, *args
    ):
        print(obj, data, args)
        data['db'] = db
    
    async def post_process(
        self, obj, data, *args
    ):
        print(obj, data, args)

if __name__ == '__main__':
    bot = Bot(token=environ.get('TOKEN'), parse_mode="HTML")
    dp = Dispatcher(bot)

    dp.middleware.setup(DBMiddleware())

    dp.register_message_handler(menu, filters.ChatTypeFilter('supergroup'), commands=['start', 'menu'])
    dp.register_message_handler(pussy, filters.Text(equals='да', ignore_case=True))

    executor.start_polling(dp, skip_updates=True, loop=loop)

