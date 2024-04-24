from aiogram import types
from loader import dp

instruction = ('<b>❗️Инструкция❗️</b>\n\n'
               '👉В пункте menu вы можете выбрать команды, или ввести их вручную:\n'
               '✅Узнать курс доллара на текущий момент /dollar_rate\n'
               '✅Получать данные периодически /receive_on_time\n'
               '✅Просмотреть историю запросов /history\n'
               '✅Посмотреть инструкцию /instruction\n'
               '✅Написать в техподдержку о проблемах в работе бота /help')


@dp.message_handler(text="/instruction")
async def command_instruction(message: types.Message):
    await message.answer(instruction)
