""" Получение курса доллара на текущий момент """

from aiogram import types
from loader import dp
from request.get_course import get_currency_rate


@dp.message_handler(text='/dollar_rate')
async def dollar_rate(message: types.Message):
    user_id = int(message.from_user.id)
    # Отправляем пользователю текущий курс доллара
    text = await get_currency_rate(user_id)
    await message.answer(text)
