from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Получать данные в определенное время",
                                                             callback_data='Получать данные в определенное время'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Отключить автоматическую отправку данных",
                                                             callback_data='Отключить автоматическую отправку данных')
                                    ]
                                ])


