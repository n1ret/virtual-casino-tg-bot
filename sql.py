import asyncpg

import asyncio
from functools import partial

from classes import User


class DatabaseConnection:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.connection = None
        self.connections_number = 0
        
    async def __aenter__(self) -> asyncpg.Connection:
        self.connections_number += 1
        if self.connection is None:
            self.connection = await asyncpg.connect(*self.args, **self.kwargs)
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.connections_number -= 1
        if self.connections_number <= 0:
            await self.connection.close()


class DataBase:
    def __init__(self, host, name, user='postgres', password=None, loop=None):
        connect_dsn = f'postgresql://{user}@{host}/{name}'
        if password:
            connect_dsn += f'?password={password}'

        self.connect = partial(DatabaseConnection, connect_dsn)

        if not loop:
            loop = asyncio.get_event_loop()
        self.loop = loop

        self.loop.run_until_complete(self.__init_db())

    async def __init_db(self):
        async with self.connect() as con:
            await con.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id bigint PRIMARY KEY,
                moneys bigint DEFAULT 0,
                reward_time timestamp DEFAULT now()
            )
            """)

    async def add_user(self, user_id: int):
        async with self.connect() as con:
            await con.execute(
                "INSERT INTO users(user_id) VALUES($1)",
                user_id
            )

    async def get_user(self, user_id: int):
        async with self.connect() as con:
            row = await con.fetchrow(
                "SELECT * FROM users WHERE user_id = $1",
                user_id
            )
            user = None
            if row:
                user = User(*row)
        return user

    async def get_or_create_user(self, user_id: int):
        async with self.connect() as con:
            await con.execute(
                "INSERT INTO users(user_id) VALUES($1) ON CONFLICT DO NOTHING",
                user_id
            )

            row = await con.fetchrow(
                "SELECT * FROM users WHERE user_id = $1",
                user_id
            )
            user = User(*row)
        return user

    async def add_money(self, user_id, amount):
        async with self.connect() as con:
            await con.execute(
                "UPDATE users SET moneys=moneys+$2 WHERE user_id=$1",
                user_id, amount
            )

    async def set_reward_datetime(self, user_id, value):
        async with self.connect() as con:
            await con.execute(
                "UPDATE users SET reward_time=$2 WHERE user_id=$1",
                user_id, value
            )

