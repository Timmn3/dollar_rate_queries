from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import admins

class Admins_message(BoundFilter):
    async def check(self, message: types.Message):
        """
        Проверяет, является ли отправитель сообщения администратором.

        Args:
            message (types.Message): Объект сообщения.

        Returns:
            bool: True, если отправитель является администратором, False в противном случае.
        """
        # Получаем ID пользователя
        user_id = int(message.from_user.id)
        # Проверяем, есть ли ID пользователя в списке администраторов
        if user_id in admins:
            return True
        else:
            return False
