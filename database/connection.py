import asyncpg

import config
from database import (
    queries,
)


class Db:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        self.pool = await asyncpg.create_pool(
                database=config.DATABASE,
                user=config.USER,
                host=config.HOST,
                password=config.PASSWORD,
        )
        config.log.info(" Есть коннект к базе")

    async def add_car(self, user_id: int | None, user_login: str | None, user_name: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                id_ = await con.fetchval(queries.insert_car, user_id, user_login, user_name)
                config.log.info(
                    f" Создана запись user_id={user_id} id={id_}, user_login={user_login}, user_name={user_name}"
                )

    async def add_mark(self, user_id: int, mark: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_field.format(field="mark"), user_id, mark)
        config.log.info(f" Добавлена марка user_id={user_id} марка={mark}")

    async def add_model(self, user_id: int, model: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_field.format(field="model"), user_id, model)
        config.log.info(f" Добавлена модель авто user_id={user_id} модель={model}")

    async def add_yaer(self, user_id: int, year: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_field.format(field="year"), user_id, year)
        config.log.info(f" Добавлен год выпуска user_id={user_id} год={year}")

    async def add_engine_volume(self, user_id: int, engine_volume: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_field.format(field="engine_volume"), user_id, engine_volume)
        config.log.info(f" Добавлен мотор/объем user_id={user_id} мотор={engine_volume}")

    async def add_engine_power(self, user_id: int, engine_power: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_field.format(field="power"), user_id, engine_power)
        config.log.info(f" Добавлена мощность авто user_id={user_id} мощность={engine_power}")

    async def add_transmission(self, user_id: int, transmission: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_field.format(field="transmission"), user_id, transmission)
        config.log.info(f" Добавлена трансмиссию авто user_id={user_id} трансмиссия={transmission}")

    async def add_city(self, user_id: int, city: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_field.format(field="city"), user_id, city)
        config.log.info(f" Добавлен город user_id={user_id} город={city}")

    # async def get_documents(self, user_id: int) -> tuple[set, set]:
    #     pics = set()
    #     docs = set()
    #     async with self.pool.acquire() as con:
    #         async with con.transaction():
    #             pics_and_docs = await con.fetch(queries.select_documents, user_id)

    #             if pics_and_docs:
    #                 pics.update(pics_and_docs[0][0])
    #                 docs.update(pics_and_docs[0][1])

    #                 if None in pics:
    #                     pics.remove(None)

    #                 if None in docs:
    #                     docs.remove(None)

    #     config.log.info(f" Для пользователя user_id={user_id} получено {len(docs)} документов и {len(pics)} фото")

    #     return pics, docs

    # async def get_summary(self, user_id: int):
    #     async with self.pool.acquire() as con:
    #         async with con.transaction():
    #             summary = await con.fetchrow(queries.select_summary, user_id)
    #             config.log.info(f" Для пользователя user_id={user_id} получено {summary}")

    #             return summary


async def init_db() -> Db:
    db = Db()
    await db.init_pool()

    async with db.pool.acquire() as con:
        async with con.transaction():
            await con.execute(queries.create_cars)

    return db
