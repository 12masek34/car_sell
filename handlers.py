from aiogram import (
    Bot,
    F,
    Router,
    types,
)
from aiogram.filters import (
    Command,
)
from aiogram.fsm.context import (
    FSMContext,
)
from aiogram_media_group import (
    media_group_handler,
)

from config import (
    CARD_NUMBER,
    GROUP_ID,
    log,
)
from constants import (
    SEND,
)
from database.connection import (
    Db,
)
from states import (
    CarState,
)
from utils import (
    get_keyboard,
    get_summary,
)


router = Router()



@router.message(F.text.lower() == SEND.lower())
async def final(message: types.Message, db: Db, bot: Bot):
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} закончил ввлодить данные по машине")
    pics, docs, videos = await db.get_documents(user_id)
    summary = await db.get_summary(user_id)
    files, result = get_summary(pics, docs, videos, summary)

    for file in files:
        await bot.send_media_group(GROUP_ID, file)

    await bot.send_message(GROUP_ID, result)

    await message.answer(
        f"Переводи деньги на {CARD_NUMBER} и я размещу твое объявление.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(Command("start"))
@router.message(F.text.lower() == "start")
async def cmd_start(message: types.Message, state: FSMContext, db: Db):
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    log.info(f" Пользователь user_id={user_id} user_name={first_name} user_login={user_name} стартует бота")
    await db.add_car(user_id, user_name, first_name)
    await message.answer("Марка", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(CarState.model)


@router.message(CarState.model)
async def model(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какая марка авто?\nВведите текстом.",
        )
        await state.set_state(CarState.model)
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
        await state.set_state(CarState.year)
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
        await state.set_state(CarState.engine_volume)
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
        await state.set_state(CarState.engine_power)
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
        await state.set_state(CarState.transmission)
        return

    engine_power = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил мощность мотора")
    await db.add_engine_power(user_id, engine_power)
    keyboard = get_keyboard("автомат", "робот", "механика")
    await message.answer("Трансмиссия", reply_markup=keyboard)
    await state.set_state(CarState.city)


@router.message(CarState.city)
async def city(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        keyboard = get_keyboard("автомат", "робот", "механика")
        await message.answer(
            "Что то не понял, какая трансмиссия?\nВведите текстом.",
            reply_markup=keyboard,
        )
        await state.set_state(CarState.city)
        return

    transmission = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил трансмиссию")
    await db.add_transmission(user_id, transmission)
    await message.answer("Город", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(CarState.contacts)


@router.message(CarState.contacts)
async def contacts(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какой город?\nВведите текстом.",
        )
        await state.set_state(CarState.contacts)
        return

    city = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил город")
    await db.add_city(user_id, city)
    await message.answer("Номер телефона/ник")
    await state.set_state(CarState.price)


@router.message(CarState.price)
async def price(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какой номер телефона/ник?\nВведите текстом.",
        )
        await state.set_state(CarState.price)
        return

    contact = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил контактные данные")
    await db.add_contact(user_id, contact)
    await message.answer("цена")
    await state.set_state(CarState.description)


@router.message(CarState.description)
async def description(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, какая цена?\nВведите текстом.",
        )
        await state.set_state(CarState.description)
        return

    price = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил цену")
    await db.add_price(user_id, price)
    await message.answer("описание")
    await state.set_state(CarState.files)


@router.message(CarState.files, F.media_group_id, F.content_type.in_({"photo", "document", "video"}))
@media_group_handler
async def catch_group_files(messages: list[types.Message], state: FSMContext, db: Db):
    user_id = None
    user_name = None

    for message in messages:
        document_id = getattr(message.document, "file_id", None)
        photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
        video_id = getattr(message.video, "file_id", None) if message.video else None
        user_id = message.from_user.id if not user_id else user_id
        user_name = message.from_user.username if not user_name else user_name
        await db.add_document(user_id, document_id, photo_id, video_id)

    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил медиафайлы")
    keyboard = get_keyboard(SEND)
    await messages[0].answer("фото/видео", reply_markup=keyboard)
    await state.set_state(CarState.files)



@router.message(CarState.files, F.content_type.in_({"photo", "document", "video"}))
async def catch_files(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None
    video_id = getattr(message.video, "file_id", None) if message.video else None
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил медиафайл")
    await db.add_document(user_id, document_id, photo_id, video_id)
    keyboard = get_keyboard(SEND)
    await message.answer("фото/видео", reply_markup=keyboard)
    await state.set_state(CarState.files)


@router.message(CarState.files)
async def files(message: types.Message, state: FSMContext, db: Db):
    document_id = getattr(message.document, "file_id", None)
    photo_id = getattr(message.photo[-1], "file_id", None) if message.photo else None

    if document_id or photo_id:
        await message.answer(
            "Что то не понял, введите описание текстом?\nВведите текстом.",
        )
        await state.set_state(CarState.files)
        return

    description = message.text
    user_id = message.from_user.id
    user_name = message.from_user.username
    log.info(f" Пользователь user_id={user_id} user_name={user_name} добавил описание")
    await db.add_description(user_id, description)
    await message.answer("фото/видео")
    await state.set_state(CarState.files)

