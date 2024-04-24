from loader import scheduler, db
from scheduler.by_time import schedule_jobs
from loguru import logger
from utils.db_api.db_gino import on_startup
from bot_send.notify_admins import on_startup_notify
from bot_send.set_bot_commands import set_default_commands
from aiogram import executor
from handlers import dp as dp_handler


async def startup(dpr):
    """
    Функция, вызываемая при запуске бота.
    """
    # Инициализация логирования в файл
    logger.add("file.log", format="{time} {level} {message}", level="DEBUG", rotation="50 MB", compression="zip")

    # Инициализация базы данных
    await on_startup(db)

    # Удаление базы данных
    # await db.gino.drop_all()

    # Создание всех таблиц и запись лога о запуске
    await db.gino.create_all()
    logger.info('Бот запущен')

    # Отправка уведомления об запуске бота администраторам
    await on_startup_notify(dpr)

    # Установка стандартных команд бота
    await set_default_commands(dpr)

    # Запуск планировщика
    await schedule_jobs()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp_handler, on_startup=startup)


