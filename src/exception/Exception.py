class ConnectionDBException(Exception):
    def __init__(self, message="Не удалось подключиться к базе данных"):
        super().__init__(message)

class JWTException(Exception):
    def __init__(self, message="Ошибка при создании токена"):
        super().__init__(message)

class NotEnoughCoinsException(ValueError):
    def __init__(self, message="Недостаточно монет для операции"):
        super().__init__(message)


class BadAuthenticateException(ValueError):
    def __init__(self, message="Неверный логин или пароль"):
        super().__init__(message)

class UserNotFoundException(ValueError):
    def __init__(self, message="Пользователь не найден"):
        super().__init__(message)

class MerchNotFoundException(ValueError):
    def __init__(self, message="Мерч не найден"):
        super().__init__(message)
class NotCorrectRequestException(ValueError):
    def __init__(self, message="Некорректный запрос"):
        super().__init__(message)
