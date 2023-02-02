import asyncpg

import asyncio

from classes import User


class DatabaseConnection(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        
    async def __aenter__(self):
        self.connection = await asyncpg.connect(*self.args, **self.kwargs)
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()


class DataBase:
    def __init__(self, host, name, user='postgres', password=None, loop=None):
        connect_dsn = f'postgresql://{user}@{host}/{name}'
        if password:
            connect_dsn += f'?password={password}'

        self.connection = DatabaseConnection(connect_dsn)

        if not loop:
            loop = asyncio.get_event@_loop()
        self.loop = loop

        self.loop.run_until_complete(self.__init_db())

    async def __init_db(self):
        async with self.connection as con:
            await con.execute("""
            CREATE TABLE IF NOT EXISTS users(
                user_id bigint PRIMARY KEY,
                moneys bigint DEFAULT 0,
                reward_time timestamp DEFAULT now()
            )
            """)

    async def add_user(self, user_id):
        async with self.connection as con:
            await con.execute(
                "INSERT INTO users(user_id) VALUES($1)",
                user_id
            )

    async def get_user(self, user_id):
        async with self.connection as con:
            row = await con.fetchrow(
                "SELECT * FROM users WHERE user_id = $1",
                user_id
            )
            user = None
            if row:
                user = User(*row)
        return user

    async def get_or_create_user(self, user_id: int):
        user = await self.get_user(user_id)
        if not user:
            await self.add_user(user_id)
            user = await self.get_user(user_id)
        return user

