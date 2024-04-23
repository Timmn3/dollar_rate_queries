from aiogram import types
from loader import dp
from utils.db_api.user_commands import get_course_history


@dp.message_handler(text='/history')
async def history(message: types.Message):
    user_id = int(message.from_user.id)
    history_text = await get_course_history(user_id)
    await message.answer(f'История запросов курса доллара:\n{history_text}')
