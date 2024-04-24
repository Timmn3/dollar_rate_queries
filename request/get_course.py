import requests
from bs4 import BeautifulSoup
from datetime import datetime
from loguru import logger

from utils.db_api.user_commands import add_course_history

async def get_currency_rate(user_id: int) -> str:
    """
    Функция для получения курса доллара к рублю с веб-сайта Google.
    :param user_id: ID пользователя.
    :return: Курс доллара к рублю в виде строки.
    """
    try:
        # Адрес сайта, с которого мы будем получать данные
        url = "https://www.google.com/search?q=курс+доллара+к+рублю"

        # Получаем содержимое страницы
        response = requests.get(url)

        # Проверяем статус ответа
        response.raise_for_status()

        # Создаем объект BeautifulSoup для парсинга HTML-разметки
        soup = BeautifulSoup(response.content, "html.parser")

        # Получаем элемент с курсом валюты
        course = soup.find("div", class_="BNeawe iBp4i AP7Wnd").get_text()

        # Оставляем только число
        amount = course.replace(",", ".").split()[0]

        result = f' 1 USD = {amount} ₽'

        # записываем запрос в БД
        value = str(datetime.now().strftime("%Y-%m-%d %H:%M")) + f' 💵{amount} ₽'
        await add_course_history(user_id, value)

        return result
    except Exception as e:
        logger.exception(f"Error occurred while fetching currency rate: {e}")
        return "Произошла ошибка при получении курса валюты."
