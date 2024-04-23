""" Получение курса доллара на текущий момент """

import re
from aiogram import types
from loader import dp


@dp.message_handler(text='/cards')
async def cards_change(message: types.Message):
    user_id = int(message.from_user.id)
    cards = await get_card_number_by_user_id(user_id)
    if cards == '0':
        await message.answer('У Вас нет активных карт, для начала пройдите регистрацию /register')
    else:
        await message.answer(f'Ваши карты: \n{cards}\n'
                             f'Выберите действие:', reply_markup=kb_cards)