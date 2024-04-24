from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from bot_send.notify_admins import new_user_registration
from handlers.users.instruction import instruction
from loader import dp
from utils.db_api import user_commands as commands
from utils.misc import rate_limit


@rate_limit(limit=3)
@dp.message_handler(CommandStart())
async def command_start(message: types.Message):
    args = message.get_args()  # Получаем аргументы из команды /start (например, id пользователя-пригласителя)
    new_args = await commands.check_args(args, message.from_user.id)  # Проверяем аргументы

    try:
        user = await commands.select_user(message.from_user.id)
        if user.status == 'active':
            await message.answer('Бот работает!')
        elif user.status == 'banned':
            await message.answer('Ты забанен')
    except Exception:
        # Если пользователь не найден, добавляем его в базу данных
        await commands.add_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            referral_id=int(new_args),  # Присваиваем аргументы в качестве пригласительного ID
            status='active',
            time_report='',
            course_history=''
        )

        # Уведомляем администраторов о новом пользователе
        await new_user_registration(
            dp=dp,
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username
        )

        try:
            # Отправляем уведомление пользователю, который пригласил нового пользователя
            await dp.bot.send_message(
                chat_id=int(new_args),
                text=f'По твоей ссылке зарегистрировался(-ась) <b>{message.from_user.first_name}</b>\n'
            )
        except Exception:
            pass

        await message.answer(f'Добро пожаловать!')
        await message.answer(instruction)  # Отправляем инструкцию новому пользователю
