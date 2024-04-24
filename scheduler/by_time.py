from datetime import datetime
from loguru import logger
from loader import scheduler, dp
from request.get_course import get_currency_rate
from utils.db_api.user_commands import get_non_empty_time_reports


async def schedule_jobs():
    """
    Запускает задачу по расписанию для отправки сообщений пользователям.
    """
    try:
        scheduler.add_job(send_message_task, 'interval', minutes=1)  # Запускаем задачу каждую минуту
    except Exception as e:
        logger.exception(f'Ошибка при добавлении задачи в расписание: {e}')


async def send_message_task():
    """
    Отправляет сообщения пользователям с курсом валюты в указанный ими момент времени.
    """
    try:
        current_time = datetime.now().strftime("%H:%M")  # Получаем текущее время в формате 'hour:minute'
        empty_time_reports = await get_non_empty_time_reports()  # Получаем словарь с непустым временем пользователей
        for user_id, course_history in empty_time_reports.items():
            # Проверяем, наступило ли заданное время для отправки сообщения пользователю
            if current_time in course_history:
                text = await get_currency_rate(user_id)  # Получаем курс валют для данного пользователя
                await dp.bot.send_message(chat_id=user_id, text=text)  # Отправляем сообщение
    except Exception as e:
        logger.exception(f'Ошибка при отправке сообщения: {e}')
