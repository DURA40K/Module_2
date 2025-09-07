# Файл с настройками и константами

# Уровни игры с количеством раундов
GAME_LEVELS = {
    "1": 5,  # Short
    "2": 8,  # Medium
    "3": 10  # Long
}

# Обратное соответствие для названий уровней
GAME_LEVELS_CONVERT = {
    5: "Short",
    8: "Medium",
    10: "Long"
}

# Настройки кубика
DICE_MIN = 1
DICE_MAX = 6

# Символы кубика 
DICE_SYMBOLS = {
    1: "⚀",
    2: "⚁", 
    3: "⚂",
    4: "⚃",
    5: "⚄",
    6: "⚅"
}

# Файл для сохранения результатов
RESULTS_FILE = "game_results.json"

# Формат даты и времени
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def clear():
    # Очистка терминала
    print('\033[2J\033[3J\033[H\033[1;1H', end='', flush=True)
