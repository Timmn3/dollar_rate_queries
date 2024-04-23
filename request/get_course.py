import requests
from bs4 import BeautifulSoup


# Функция для получения курса валюты
def get_currency_rate():
    """
    Функция для получения курса валюты
    :return: string
    """

    # Адрес сайта, с которого мы будем получать данные
    url = "https://www.google.com/search?q=курс+доллара+к+рублю"

    # Получаем содержимое страницы
    response = requests.get(url)

    # Создаем объект BeautifulSoup для парсинга HTML-разметки
    soup = BeautifulSoup(response.content, "html.parser")

    # Получаем элемент с курсом валюты
    course = soup.find("div", class_="BNeawe iBp4i AP7Wnd").get_text()

    # Оставляем только число
    amount = course.replace(",", ".").split()[0]

    # делаем в каком значении нужно
    result = f' 1 USD = {amount} ₽'

    return result
