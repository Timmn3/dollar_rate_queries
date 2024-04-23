from asyncpg import UniqueViolationError
from loguru import logger
from utils.db_api.db_gino import db
from utils.db_api.shemas.user import User


# добавление пользователя
async def add_user(user_id: int, first_name: str, last_name: str, username: str, referral_id: int, status: str,
                   subscription: float, course_history: str):
    try:
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                    referral_id=referral_id, status=status, subscription=subscription, course_history=course_history)
        await user.create()
    except UniqueViolationError:
        logger.exception('Пользователь не добавлен')


# выбрать всех пользователей
async def select_all_users():
    users = await User.query.gino.all()
    return users


# подсчет количества пользователей
async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


# выбрать пользователя
async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


# функция для проверки аргументов переданных при регистрации
async def check_args(args, user_id: int):
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
        # получаем из БД пользователя у которого user_id такой же как и переданный аргумент
        elif await select_user(user_id=int(args)) is None:  # если его нет
            args = '0'
            return args

        else:  # если аргумент прошел все проверки
            args = str(args)
            return args

    else:  # есл  что то пошло не так
        args = '0'
        return args


async def user_bill_id(user_id: int):  # получаем идентификатор заказа
    user = await select_user(user_id)  # получаем юзера
    return user.bill_id


async def change_bill_id(user_id: int, value):  # измененяем идентификатор заказа
    user = await select_user(user_id)
    new_bill_id = value
    await user.update(bill_id=new_bill_id).apply()


async def clear_bill_id(user_id: int):  # очищаем идентификатор заказа
    user = await select_user(user_id)
    await user.update(bill_id='').apply()
