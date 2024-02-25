from aiogram.fsm.state import (
    State,
    StatesGroup,
)


class CarState(StatesGroup):
    mark = State()
    model = State()
    year = State()
    engine_volume = State()
    engine_power = State()
    transmission = State()
    city = State()
    contacts = State()
    price = State()
    description = State()
    files = State()
