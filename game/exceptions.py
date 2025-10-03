
class InvalidInputError(Exception):
    # Исключение для некорректного ввода пользователя
    pass


class InvalidRollError(Exception):
    # Исключение для неправильного броска кубика
    pass


class ExitToMenuError(Exception):
    # Исключение для выхода в главное меню без сохранения
    pass
