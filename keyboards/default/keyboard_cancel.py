from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)