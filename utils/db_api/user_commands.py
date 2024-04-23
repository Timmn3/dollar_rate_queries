from asyncpg import UniqueViolationError
from loguru import logger
from utils.db_api.db_gino import db
from utils.db_api.shemas.user import User


# добавление пользователя
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
    users = await User.query.gino.all()
    return users


async def count_users():
    """ Подсчет количества пользователей """
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def select_user(user_id):
    """ Выбрать пользователя """
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def check_args(args, user_id: int):
    """ Проверка аргументов переданных при регистрации """
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


async def get_time_report(user_id: int):
    """ Получение времени отчета для пользователя """
    user = await select_user(user_id)  # получаем юзера
    return user.daily_report


async def change_time_report(user_id: int, value: str):
    """ Изменяем значение отчета пользователю """
    user = await select_user(user_id)
    new_time_report = value
    await user.update(time_report=new_time_report).apply()


async def clear_time_report(user_id: int):
    """ Очищаем поле отчета по времени"""
    user = await select_user(user_id)
    await user.update(time_report='').apply()
