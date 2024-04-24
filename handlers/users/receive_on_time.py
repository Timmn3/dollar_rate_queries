from aiogram import types
from aiogram.dispatcher import FSMContext
import re
from loguru import logger
from keyboards.default import button_cancel
from keyboards.inline import ikb_menu
from loader import dp
from states import Receipt
from utils.db_api.user_commands import change_time_report
from datetime import datetime, timedelta


@dp.message_handler(text='/receive_on_time')
async def dollar_rate(message: types.Message):
    """
    Обработчик команды /receive_on_time.

    Предоставляет пользователю возможность выбрать способ получения уведомлений о курсе доллара.

    Args:
        message (types.Message): Объект сообщения.

    Returns:
        None
    """
    try:
        await message.answer('Выберите как хотите получать уведомления:', reply_markup=ikb_menu)
    except Exception as e:
        logger.exception(f'Ошибка при выполнении команды /receive_on_time: {e}')


@dp.callback_query_handler(text='receive_data_at_specified_intervals')
async def frequency_report(call: types.CallbackQuery):
    """
    Обработчик запроса на получение данных с заданной периодичностью.

    Args:
        call (types.CallbackQuery): Объект запроса обратного вызова.

    Returns:
        None
    """
    try:
        await call.message.answer('С какой периодичностью Вы хотите получать информацию о курсе доллара, '
                                  'введите количество минут (например 60):',
                                  reply_markup=button_cancel)
        await Receipt.frequency_report.set()  # устанавливаем состояние для установки времени
        await call.message.edit_reply_markup()  # убрать клавиатуру
        await call.message.delete()  # удаляем сообщение 'Выберите как хотите получать уведомления'
    except Exception as e:
        logger.exception(f'Ошибка при обработке запроса на получение данных с заданной периодичностью: {e}')


@dp.message_handler(state=Receipt.frequency_report)
async def time_report(message: types.Message, state: FSMContext):
    """
    Обработчик ввода пользователем времени для получения данных с заданной периодичностью.

    Args:
        message (types.Message): Объект сообщения.
        state (FSMContext): Контекст конечного автомата.

    Returns:
        None
    """
    try:
        set_time = message.text
        if set_time.lower() == "отмена":
            await state.finish()
            await message.answer('Отменено')
        elif not set_time.isdigit():
            await message.answer("Пожалуйста, введите только цифры для количества минут.",
                                 reply_markup=button_cancel)
        elif int(set_time) > 1440:
            await message.answer("Количество минут не должно превышать 1440 (количество минут в сутках).",
                                 reply_markup=button_cancel)
        else:
            user_id = int(message.from_user.id)
            notification_times = await generate_time_intervals(int(set_time))
            # записываем значение в БД
            await change_time_report(user_id, notification_times)
            await message.answer(f'👉Теперь Вы будете получать уведомления о курсе доллара каждые '
                                 f'<b>{set_time}</b> минут')
            await state.finish()
    except Exception as e:
        logger.exception(f'Ошибка при обработке времени для получения данных с заданной периодичностью: {e}')


async def generate_time_intervals(interval_minutes) -> str:
    """
    Генерирует строку, содержащую временные интервалы с указанным интервалом в минутах.

    Args:
        interval_minutes (int): Интервал в минутах.

    Returns:
        str: Строка, содержащая временные интервалы в формате 'ЧЧ:ММ', разделенные запятой.
    """
    try:
        current_time = datetime.now().replace(second=0, microsecond=0)
        start_time = current_time - timedelta(minutes=current_time.minute % interval_minutes)
        end_time = start_time + timedelta(hours=24)

        time_intervals = []

        while start_time < end_time:
            time_intervals.append(start_time.strftime('%H:%M'))
            start_time += timedelta(minutes=interval_minutes)

        return ", ".join(time_intervals)
    except Exception as e:
        logger.exception(f'Ошибка при генерации временных интервалов: {e}')


@dp.callback_query_handler(text='receive_data_at_a_specific_time')
async def receive_data_hours(call: types.CallbackQuery):
    """
    Обработчик запроса на получение данных в определенное время.

    Args:
        call (types.CallbackQuery): Объект запроса обратного вызова.

    Returns:
        None
    """
    try:
        await call.message.answer('В какое время Вы хотите получать информацию о курсе доллара, '
                                  'введите время через запятую (например 08:45, 10:00, 15:00):',
                                  reply_markup=button_cancel)
        await Receipt.hours_report.set()  # устанавливаем состояние для установки времени
        await call.message.edit_reply_markup()  # убрать клавиатуру
        await call.message.delete()  # удаляем сообщение 'Выберите как хотите получать уведомления'
    except Exception as e:
        logger.exception(f'Ошибка при обработке запроса на получение данных в определенное время: {e}')


@dp.message_handler(state=Receipt.hours_report)
async def time_report(message: types.Message, state: FSMContext):
    """
    Обработчик ввода пользователем времени для получения данных в определенное время.

    Args:
        message (types.Message): Объект сообщения.
        state (FSMContext): Контекст конечного автомата.

    Returns:
        None
    """
    try:
        set_times = message.text
        if set_times.lower() == "отмена":
            await state.finish()
            await message.answer('Отменено')
        else:
            # Проверяем, соответствует ли введенная строка формату "часы:минуты, часы:минуты, ..."
            time_pattern = re.compile(r'^(\d{1,2}:\d{2},\s?)*\d{1,2}:\d{2}$')
            if not time_pattern.match(set_times):
                await message.answer("Пожалуйста, введите время в формате 'часы:минуты', разделенные запятой.",
                                     reply_markup=button_cancel)
                return

            user_id = int(message.from_user.id)
            # Записываем значение в БД
            await change_time_report(user_id, set_times)
            await message.answer(f'👉Теперь Вы будете получать уведомления о курсе доллара ежедневно в '
                                 f'<b>{set_times}</b>')
            await state.finish()
    except Exception as e:
        logger.exception(f'Ошибка при обработке времени для получения данных в определенное время: {e}')


@dp.callback_query_handler(text='disable_automatic_data_submission')
async def disable_data_submission(call: types.CallbackQuery):
    """
    Обработчик запроса на отключение автоматической отправки данных.

    Args:
        call (types.CallbackQuery): Объект запроса обратного вызова.

    Returns:
        None
    """
    try:
        user_id = int(call.from_user.id)
        await change_time_report(user_id, '')
        await call.message.answer('👍Вы отписались от автоматической рассылки уведомлений о курсе доллара')
        await call.message.edit_reply_markup()  # убрать клавиатуру
        await call.message.delete()  # удаляем сообщение 'Выберите как хотите получать уведомления'
    except Exception as e:
        logger.exception(f'Ошибка при отключении автоматической отправки данных: {e}')
