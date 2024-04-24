import logging
from aiogram import Dispatcher
from data.config import admins
from utils.db_api.user_commands import count_users


async def on_startup_notify(dp: Dispatcher):
    """
    Уведомление администраторов о запуске бота.

    Args:
        dp (Dispatcher): Экземпляр Dispatcher из aiogram.
    """
    for admin in admins:
        try:
            text = 'DollarSenseBot запущен'
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)


async def new_user_registration(dp: Dispatcher, user_id, first_name, username):
    """
    Уведомление администраторов о регистрации нового пользователя.

    Args:
        dp (Dispatcher): Экземпляр Dispatcher из aiogram.
        user_id (int): ID нового пользователя.
        first_name (str): Имя нового пользователя.
        username (str): Имя пользователя в Telegram.
    """
    count = await count_users()
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=admin, text=f'✅Зарегистрирован новый пользователь:\n'
                                                          f'user_id: {user_id}\n'
                                                          f'first_name: {first_name}\n'
                                                          f'username: {username}\n'
                                                          f'🚹Всего пользователей: <b>{count}</b>')
        except Exception as err:
            logging.exception(err)


async def send_admins(dp: Dispatcher, text):
    """
    Отправка сообщения всем администраторам.

    Args:
        dp (Dispatcher): Экземпляр Dispatcher из aiogram.
        text (str): Текст сообщения.
    """
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)
