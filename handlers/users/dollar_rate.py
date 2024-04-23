""" Получение курса доллара на текущий момент """

from aiogram import types
from loader import dp
from request.get_course import get_currency_rate


@dp.message_handler(text='/dollar_rate')
async def dollar_rate(message: types.Message):
    # Отправляем пользователю текущий курс доллара
    text = get_currency_rate()
    await message.answer(text)
