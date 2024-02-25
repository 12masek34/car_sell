from aiogram.enums import (
    ParseMode,
)
from aiogram.types import (
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from asyncpg import (
    Record,
)


def get_keyboard(*args) -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(text=text) for text in args]

    return ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)


def get_summary(pics: set, docs: set, videos: set, summary: Record) -> tuple[list, str]:
    user_login = summary["user_login"]
    user_login = f"с ником @{user_login}" if user_login else "ник пользователя отсутствует"
    user_name = summary["user_name"]
    mark = summary["mark"]
    model = summary["model"]
    year = summary["year"]
    engine_volume = summary["engine_volume"]
    power = summary["power"]
    transmission = summary["transmission"]
    city = summary["city"]
    contacts = summary["contacts"]
    price = summary["price"]
    description = summary["description"]

    caption = (
        f"Пользователь по имени {user_name} {user_login} хочет разместить лялю!\n\n"
        f"Марка: {mark}\n"
        f"Модель: {model}\n"
        f"год выпуска: {year}\n"
        f"мотор/объем: {engine_volume}\n"
        f"мощность: {power}\n"
        f"трансмиссия: {transmission}\n"
        f"город: {city}\n"
        f"контакты: {contacts}\n"
        f"цена: {price}\n"
        f"описание:\n{description}\n"
    )
    files = []

    files.extend([InputMediaPhoto(media=pic) for pic in pics])
    files.extend([InputMediaDocument(media=doc) for doc in docs])
    files.extend([InputMediaVideo(media=video) for video in videos])

    if files:
        files = chunk_list(files, 9)
    else:
        files = [files]

    files.reverse()

    return files, caption


def chunk_list(input_list: list, chunk_size: int) -> list:
    chunked_list = []
    for i in range(0, len(input_list), chunk_size):
        chunked_list.append(input_list[i:i + chunk_size])

    return chunked_list
