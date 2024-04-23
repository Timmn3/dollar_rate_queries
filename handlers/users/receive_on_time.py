""" Получать данные периодически """

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import button_cancel
from keyboards.inline import ikb_menu
from loader import dp
from states import Receipt
from utils.db_api.user_commands import change_time_report


@dp.message_handler(text='/dollar_rate')
async def dollar_rate(message: types.Message):
    await message.answer('Выберите как хотите получать уведомления:', reply_markup=ikb_menu)


@dp.callback_query_handler(text='Получать данные в определенное время')
async def receive_data_hours(call: types.CallbackQuery):
    await call.message.answer('В какое время Вы хотите получать информацию о курсе доллара, '
                              'введите время через запятую (например 08:45, 10:00, 15:00):',
                              reply_markup=button_cancel)
    await Receipt.hours_report.set()  # устанавливаем состояние для установки времени
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.delete()  # удаляем сообщение 'Выберите как хотите получать уведомления'


# Отлавливаем состояние введенного времени
@dp.message_handler(state=Receipt.hours_report)
async def time_report(message: types.Message, state: FSMContext):
    set_time = message.text
    if set_time == "Oтмена":
        await state.finish()
        await message.answer('Отменено')
    else:
        user_id = int(message.from_user.id)
        # записываем значение в БД
        await change_time_report(user_id, set_time)
        await message.answer(f'👉Теперь Вы будете получать уведомления о курсе доллара ежедневно в: '
                             f'<b>{set_time}</b>')


@dp.callback_query_handler(text='Отключить автоматическую отправку данных')
async def disable_data_submission(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await change_time_report(user_id, '')
    await call.message.answer('👍Вы отписались от автоматической рассылки уведомлений о курсе доллара')
    await call.message.edit_reply_markup()  # убрать клавиатуру
    await call.message.delete()  # удаляем сообщение 'Выберите как хотите получать уведомления'

