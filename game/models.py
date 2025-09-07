# Модели для игры
# Содержит классы Player и Computer

import random
from .settings import DICE_MIN, DICE_MAX


class Player:
    # Класс игрока
    
    def __init__(self, name):
        # Инициализация игрока
        self.name = name
        self.score = 0
    
    def roll_dice(self):
        # Бросок кубика для игрока
        return random.randint(DICE_MIN, DICE_MAX)
    
    def add_score(self, points):
        # Добавляет очки к счету игрока
        self.score += points
    
    def get_score(self):
        # Возвращает текущий счет игрока
        return self.score
    
    def get_name(self):
        # Возвращает имя игрока
        return self.name
    
    def __str__(self):
        # Строковое представление игрока
        return f"Игрок: {self.name}, Счет: {self.score}"


class Computer:
    # Класс компьютера
    
    def __init__(self, name="Компьютер"):
        # Инициализация компьютера
        self.name = name
        self.score = 0
    
    def roll_dice(self):
        # Бросок кубика для компьютера
        return random.randint(DICE_MIN, DICE_MAX)
    
    def add_score(self, points):
        # Добавляет очки к счету компьютера
        self.score += points
    
    def get_score(self):
        # Возвращает текущий счет компьютера
        return self.score
    
    def get_name(self):
        # Возвращает имя компьютера
        return self.name
    
    def __str__(self):
        # Строковое представление компьютера
        return f"Компьютер: {self.name}, Счет: {self.score}"
