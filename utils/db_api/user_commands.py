from asyncpg import UniqueViolationError
from loguru import logger
from utils.db_api.db_gino import db
from utils.db_api.shemas.user import User


async def add_user(user_id: int, first_name: str, last_name: str, username: str, referral_id: int, status: str,
                   time_report: str, course_history: str):
    """
    Добавление нового пользователя в базу данных.

    Args:
        user_id (int): ID пользователя.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        username (str): Имя пользователя в Telegram.
        referral_id (int): ID пользователя, который пригласил данного пользователя.
        status (str): Статус пользователя.
        time_report (str): Отчеты по времени пользователя.
        course_history (str): История запросов курсов пользователя.

    Raises:
        UniqueViolationError: Если пользователь с таким ID уже существует в базе данных.
    """
    try:
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                    referral_id=referral_id, status=status, time_report=time_report, course_history=course_history)
        await user.create()
    except UniqueViolationError:
        logger.exception('Пользователь не добавлен')


async def select_all_users():
    """Выбрать всех пользователей."""
    try:
        users = await User.query.gino.all()
        return users
    except Exception as e:
        logger.exception(f'Ошибка при выборе всех пользователей: {e}')


async def count_users():
    """Подсчет количества пользователей."""
    try:
        count = await db.func.count(User.user_id).gino.scalar()
        return count
    except Exception as e:
        logger.exception(f'Ошибка при подсчете пользователей: {e}')


async def select_user(user_id):
    """Выбрать пользователя по его ID."""
    try:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user
    except Exception as e:
        logger.exception(f'Ошибка при выборе пользователя: {e}')


async def check_args(args, user_id: int):
    """
    Проверка аргументов, переданных при регистрации.

    Args:
        args (str): Аргументы, переданные при регистрации.
        user_id (int): ID пользователя.

    Returns:
        str: Проверенные аргументы.

    Notes:
        Если аргументы не прошли проверку, возвращается '0'.
    """
    try:
        if args == '':
            args = '0'
            return args
        elif not args.isnumeric():
            args = '0'
            return args
        elif args.isnumeric():
            if int(args) == user_id:
                args = '0'
                return args
            elif await select_user(user_id=int(args)) is None:
                args = '0'
                return args
            else:
                args = str(args)
                return args
        else:
            args = '0'
            return args
    except Exception as e:
        logger.exception(f'Ошибка при проверке аргументов: {e}')


async def get_time_report(user_id: int) -> str:
    """
    Получение временного отчета для пользователя.

    Args:
        user_id (int): ID пользователя.

    Returns:
        str: Временной отчет пользователя.
    """
    try:
        user = await select_user(user_id)
        return user.time_report
    except Exception as e:
        logger.exception(f'Ошибка при получении временного отчета: {e}')


async def change_time_report(user_id: int, value: str):
    """
    Изменение значения временного отчета пользователя.

    Args:
        user_id (int): ID пользователя.
        value (str): Новое значение временного отчета.
    """
    try:
        user = await select_user(user_id)
        new_time_report = value
        await user.update(time_report=new_time_report).apply()
    except Exception as e:
        logger.exception(f'Ошибка при изменении отчета: {e}')


async def clear_time_report(user_id: int):
    """
    Очистка поля временного отчета пользователя.

    Args:
        user_id (int): ID пользователя.
    """
    try:
        user = await select_user(user_id)
        await user.update(time_report='').apply()
    except Exception as e:
        logger.exception(f'Ошибка при очистке отчета: {e}')


async def get_non_empty_time_reports() -> dict:
    """
    Получение непустых отчетов времени для пользователей.

    Returns:
        dict: Словарь с ID пользователя в качестве ключа и непустым временным отчетом в качестве значения.
    """
    try:
        users = await select_all_users()
        non_empty_time_reports = {}
        for user in users:
            if user.time_report and user.time_report.strip():
                non_empty_time_reports[user.user_id] = user.time_report
        return non_empty_time_reports
    except Exception as e:
        logger.exception(f'Ошибка при получении непустых отчетов времени: {e}')


async def add_course_history(user_id: int, value: str):
    """
    Добавление нового запроса в историю курсов пользователя.

    Args:
        user_id (int): ID пользователя.
        value (str): Новый запрос курса.

    Raises:
        Exception: Если произошла ошибка при добавлении курса в историю.
    """
    try:
        user = await select_user(user_id)
        current_course_history = user.course_history if user.course_history else ''
        history_lines = current_course_history.split('\n')
        history_lines.append(value)
        updated_history = '\n'.join(history_lines[-100:])
        await user.update(course_history=updated_history).apply()
    except Exception as e:
        logger.exception(f'Ошибка при добавлении курса в историю: {e}')


async def get_course_history(user_id: int) -> str:
    """
    Получение истории курсов для пользователя.

    Args:
        user_id (int): ID пользователя.

    Returns:
        str: История курсов пользователя.
    """
    try:
        user = await select_user(user_id)
        return user.course_history
    except Exception as e:
        logger.exception(f'Ошибка при получении истории курсов: {e}')
