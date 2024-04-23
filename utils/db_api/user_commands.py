from asyncpg import UniqueViolationError
from loguru import logger
from utils.db_api.db_gino import db
from utils.db_api.shemas.user import User


async def add_user(user_id: int, first_name: str, last_name: str, username: str, referral_id: int, status: str,
                   time_report: str, course_history: str):
    try:
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                    referral_id=referral_id, status=status, time_report=time_report, course_history=course_history)
        await user.create()
    except UniqueViolationError:
        logger.exception('Пользователь не добавлен')


async def select_all_users():
    """ Выбрать всех пользователей """
    try:
        users = await User.query.gino.all()
        return users
    except Exception as e:
        logger.exception(f'Ошибка при выборе всех пользователей: {e}')


async def count_users():
    """ Подсчет количества пользователей """
    try:
        count = await db.func.count(User.user_id).gino.scalar()
        return count
    except Exception as e:
        logger.exception(f'Ошибка при подсчете пользователей: {e}')


async def select_user(user_id):
    """ Выбрать пользователя """
    try:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user
    except Exception as e:
        logger.exception(f'Ошибка при выборе пользователя: {e}')


async def check_args(args, user_id: int):
    """ Проверка аргументов переданных при регистрации """
    try:
        if args == '':  # если в аргумент передана пустая строка
            args = '0'
            return args
        elif not args.isnumeric():  # если не только цифры, а и буквы
            args = '0'
            return args
        elif args.isnumeric():  # если только цифры
            if int(args) == user_id:  # если аргумент является id пользователя
                args = '0'
                return args
            # получаем из БД пользователя у которого user_id такой же, как и переданный аргумент
            elif await select_user(user_id=int(args)) is None:  # если его нет
                args = '0'
                return args
            else:  # если аргумент прошел все проверки
                args = str(args)
                return args
        else:  # если что-то пошло не так
            args = '0'
            return args
    except Exception as e:
        logger.exception(f'Ошибка при проверке аргументов: {e}')


async def get_time_report(user_id: int) -> str:
    """ Получение времени отчета для пользователя """
    try:
        user = await select_user(user_id)  # получаем юзера
        return user.time_report
    except Exception as e:
        logger.exception(f'Ошибка при получении времени отчета: {e}')


async def change_time_report(user_id: int, value: str):
    """ Изменяем значение отчета пользователю """
    try:
        user = await select_user(user_id)
        new_time_report = value
        await user.update(time_report=new_time_report).apply()
    except Exception as e:
        logger.exception(f'Ошибка при изменении отчета: {e}')


async def clear_time_report(user_id: int):
    """ Очищаем поле отчета по времени"""
    try:
        user = await select_user(user_id)
        await user.update(time_report='').apply()
    except Exception as e:
        logger.exception(f'Ошибка при очистке отчета: {e}')


async def add_course_history(user_id: int, value: str):
    """ Добавляем новую строку к истории курсов для пользователя """
    try:
        user = await select_user(user_id)
        current_course_history = user.course_history if user.course_history else ''
        new_course_history = '\n'.join([current_course_history, value])
        await user.update(course_history=new_course_history).apply()
    except Exception as e:
        logger.exception(f'Ошибка при добавлении курса в историю: {e}')


async def get_course_history(user_id: int) -> str:
    """ Получение истории курсов для пользователя """
    try:
        user = await select_user(user_id)
        return user.course_history
    except Exception as e:
        logger.exception(f'Ошибка при получении истории курсов: {e}')
