def rate_limit(limit: int, key=None):
    """
    Декоратор для настройки ограничения скорости выполнения функции.

    Args:
        limit (int): Максимальное количество раз, которое функция может быть вызвана за определенный период времени.
        key (str, optional): Ключ, используемый для идентификации пользователя или контекста, если ограничение скорости
                             применяется для разных пользователей или сценариев. По умолчанию None.

    Returns:
        function: Декорированная функция с установленным ограничением скорости.

    Examples:
        Пример использования декоратора с ограничением скорости в 3 вызова в минуту:

        @rate_limit(limit=3)
        async def my_function():
            pass

        В этом примере функция `my_function` может быть вызвана не более 3 раз в течение каждой минуты.

        Пример использования декоратора с ограничением скорости и ключом:

        @rate_limit(limit=5, key='user_id')
        async def my_function(user_id: int):
            pass

        В этом примере функция `my_function` может быть вызвана не более 5 раз в минуту для каждого `user_id`.
    """
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator
