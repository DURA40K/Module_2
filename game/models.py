# Модели для игры
# Содержит абстрактный класс GameParticipant и классы Player и Computer

import random
from abc import ABC, abstractmethod
from .settings import DICE_MIN, DICE_MAX


class GameParticipant(ABC):
    # Абстрактный класс для участников игры
    
    def __init__(self, name):
        # Инициализация участника игры
        self.name = name
        self.score = 0
    
    @abstractmethod
    def get_display_name(self):
        # Абстрактный метод для получения отображаемого имени
        pass
    
    def roll_dice(self):
        # Бросок кубика (одинаков для всех участников)
        return random.randint(DICE_MIN, DICE_MAX)
    
    def add_score(self, points):
        # Добавляет очки к счету участника
        self.score += points
    
    def get_score(self):
        # Возвращает текущий счет участника
        return self.score
    
    def get_name(self):
        # Возвращает имя участника
        return self.name
    
    def reset_score(self):
        # Сброс счета участника
        self.score = 0


class Player(GameParticipant):
    # Класс игрока, наследуется от GameParticipant
    
    def __init__(self, name):
        # Инициализация игрока
        super().__init__(name)
    
    def get_display_name(self):
        # Возвращает отображаемое имя игрока
        return f"Игрок: {self.name}"
    
    def __str__(self):
        # Строковое представление игрока
        return f"Игрок: {self.name}, Счет: {self.score}"


class Computer(GameParticipant):
    # Класс компьютера, наследуется от GameParticipant
    
    def __init__(self, name="Компьютер"):
        # Инициализация компьютера
        super().__init__(name)
    
    def get_display_name(self):
        # Возвращает отображаемое имя компьютера
        return f"Компьютер: {self.name}"
    
    def __str__(self):
        # Строковое представление компьютера
        return f"Компьютер: {self.name}, Счет: {self.score}"
