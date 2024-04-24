from aiogram import types


#  Установка стандартных команд для бота
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Старт'),
        types.BotCommand('dollar_rate', 'Курс доллара'),
        types.BotCommand('receive_on_time', 'Получать курс доллара периодически'),
        types.BotCommand('history', 'История запросов курса доллара'),
        types.BotCommand('instruction', 'Инструкция'),
        types.BotCommand('help', 'Техподдержка'),
    ])
