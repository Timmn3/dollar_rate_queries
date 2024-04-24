from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text="Получать данные с заданной периодичностью",
                                                             callback_data='receive_data_at_specified_intervals'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Получать данные в определенное время",
                                                             callback_data='receive_data_at_a_specific_time'),
                                    ],
                                    [
                                        InlineKeyboardButton(text="Отключить автоматическую отправку данных",
                                                             callback_data='disable_automatic_data_submission')
                                    ]
                                ])
