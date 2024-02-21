from aiogram import (
    Bot,
    F,
    Router,
    types,
)
from aiogram.enums import ParseMode
from aiogram.filters import (
    Command,
)
from aiogram.fsm.context import (
    FSMContext,
)

from config import (
    GROUP_ID,
    log,
)
from database.connection import (
    Db,
)
from states import (
    CarState,
)


router = Router()


@router.message(Command("start"))
@router.message(F.text.lower() == "start")
async def cmd_start(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    log.info(f" Пользователь user_id={user_id} user_name={first_name} user_login={user_name} стартует бота")
    await db.add_car(user_id, user_name, first_name)
    await message.answer("Марка")
    await state.set_state(CarState.model)


@router.message(CarState.model)
async def model(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какая марка авто?\nВведите текстом.",
        )
        await state.set_state(CarState.mark)
        return

    mark = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил марку авто")
    await db.add_mark(user_id, mark)
    await message.answer("Модель")
    await state.set_state(CarState.year)


@router.message(CarState.year)
async def year(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какая модель авто?\nВведите текстом.",
        )
        await state.set_state(CarState.model)
        return

    model = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил модель авто")
    await db.add_model(user_id, model)
    await message.answer("Год")
    await state.set_state(CarState.engine_volume)


@router.message(CarState.engine_volume)
async def volume(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какой год авто?\nВведите текстом.",
        )
        await state.set_state(CarState.year)
        return

    year = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил год выпуска")
    await db.add_yaer(user_id, year)
    await message.answer("Мотор/объем")
    await state.set_state(CarState.engine_power)


@router.message(CarState.engine_power)
async def power(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какой мотор/объем?\nВведите текстом.",
        )
        await state.set_state(CarState.engine_volume)
        return

    engine_volume = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил мотор/объем")
    await db.add_engine_volume(user_id, engine_volume)
    await message.answer("Мощность")
    await state.set_state(CarState.transmission)


@router.message(CarState.transmission)
async def transmission(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какая мощность?\nВведите текстом.",
        )
        await state.set_state(CarState.engine_power)
        return

    engine_power = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил мощность мотора")
    await db.add_engine_power(user_id, engine_power)
    await message.answer("Трансмиссия")
    await state.set_state(CarState.city)


@router.message(CarState.city)
async def city(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какая трансмиссия?\nВведите текстом.",
        )
        await state.set_state(CarState.transmission)
        return

    transmission = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил трансмиссию")
    await db.add_transmission(user_id, transmission)
    await message.answer("Город")
    await state.set_state(CarState.contacts)


@router.message(CarState.contacts)
async def contacts(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какой город?\nВведите текстом.",
        )
        await state.set_state(CarState.transmission)
        return

    city = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил город")
    await db.add_city(user_id, city)
    await message.answer("Номер телефона/ник")
    await state.set_state(CarState.price)
