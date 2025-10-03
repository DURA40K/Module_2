# Основная логика игры - классы Game и GameUI

import time
from datetime import datetime
from .models import Player, Computer
from .settings import (GAME_LEVELS, DICE_SYMBOLS, DATE_FORMAT, clear,
                       YES_ANSWERS, NO_ANSWERS, EXIT_ANSWERS, validate_player_name, get_level_name)
from .exceptions import InvalidInputError, ExitToMenuError
from .score import ScoreManager


class GameUI:
    # Класс для управления пользовательским интерфейсом
    
    @staticmethod
    def confirm_exit_to_menu():
        # Запрашивает подтверждение выхода в главное меню
        clear()
        print("⚠️  ВНИМАНИЕ!")
        print("Вы уверены, что хотите выйти в главное меню?")
        print("Результат игры НЕ будет сохранен!")
        print()
        
        while True:
            try:
                choice = input("Подтвердите выход (y/n): ").strip().lower()
                if choice in YES_ANSWERS:
                    return True
                elif choice in NO_ANSWERS:
                    return False
                else:
                    print("Введите 'y' для подтверждения или 'n' для отмены.")
            except KeyboardInterrupt:
                return True
    
    @staticmethod
    def get_player_name():
        # Получает имя игрока
        while True:
            try:
                clear()
                name = input("\nВведите ваше имя (1 - выход в меню): ").strip()
                if name in EXIT_ANSWERS:
                    if GameUI.confirm_exit_to_menu():
                        raise ExitToMenuError("Выход в главное меню")
                    else:
                        continue
                validate_player_name(name)
                return name
            except InvalidInputError as e:
                print(f"Ошибка: {e}")
                input("Нажмите Enter для продолжения...")
    
    @staticmethod
    def get_game_level():
        # Получает уровень игры от пользователя
        while True:
            try:
                clear()
                print("\nВыберите уровень игры:")
                print("1. Короткая игра (5 раундов)")
                print("2. Средняя игра (8 раундов)")
                print("3. Длинная игра (10 раундов)")
                print("4. Вернуться в главное меню")
                
                choice = input("Ваш выбор (1-4): ").strip()
                
                if choice == "4":
                    if GameUI.confirm_exit_to_menu():
                        raise ExitToMenuError("Выход в главное меню")
                    else:
                        continue
                
                if choice not in GAME_LEVELS:
                    raise InvalidInputError("Неверный выбор! Введите число от 1 до 4.")
                
                return choice
                
            except InvalidInputError as e:
                print(f"Ошибка: {e}")
                input("Нажмите Enter для продолжения...")
    
    @staticmethod
    def get_dice_roll_input(round_number):
        # Обрабатывает ввод для броска кубика
        while True:
            try:
                user_input = input("Нажмите Enter для броска кубика (1 - выход в меню): ")
                if user_input == "":
                    return True
                elif user_input in EXIT_ANSWERS:
                    if GameUI.confirm_exit_to_menu():
                        raise ExitToMenuError("Выход в главное меню")
                    else:
                        clear()
                        print(f"\n{'='*20} РАУНД {round_number} {'='*20}")
                        print("\nВаш ход:")
                        continue
                else:
                    print("Бросок не сделан!!! Нажмите \"Enter\" для повторного броска или '1' для выхода.")
            except KeyboardInterrupt:
                if GameUI.confirm_exit_to_menu():
                    raise ExitToMenuError("Выход в главное меню")
    
    @staticmethod
    def check_exit_to_menu():
        # Проверяет, хочет ли пользователь выйти в главное меню
        while True:
            try:
                choice = input("Нажмите Enter для продолжения (1 - выход в меню): ").strip()
                if choice == "":
                    clear()
                    return
                elif choice in EXIT_ANSWERS:
                    if GameUI.confirm_exit_to_menu():
                        raise ExitToMenuError("Выход в главное меню")
                    else:
                        clear()
                        return
                else:
                    print("Нажмите Enter для продолжения или '1' для выхода в меню.")
            except KeyboardInterrupt:
                if GameUI.confirm_exit_to_menu():
                    raise ExitToMenuError("Выход в главное меню")


class Game:
    # Основной класс игры
    
    def __init__(self):
        # Инициализация игры
        self.player = None
        self.computer = Computer()
        self.rounds_total = 0
        self.current_round = 0
        self.start_time = None
        self.ui = GameUI()
        self.score_manager = ScoreManager()
    
    def initialize_game(self):
        # Инициализирует новую игру
        print("\n🎲 Добро пожаловать в игру 'КОСТИ'! 🎲")
        print("Вам предстоит сразиться с компьютером в броске кубиков!")
        
        player_name = self.ui.get_player_name()
        level_choice = self.ui.get_game_level()
        
        self.player = Player(player_name)
        self.rounds_total = GAME_LEVELS[level_choice]
        self.current_round = 0
        self.start_time = datetime.now()
        
        level_name = get_level_name(self.rounds_total)
        clear()
        print(f"\nВыбран уровень: {level_name} ({self.rounds_total} раундов)")
        input("Нажмите Enter для начала игры...")
        clear()
        
        print(f"\n🎮 Игра начинается! Удачи, {player_name}!")
        time.sleep(1)
    
    def play_round(self):
        # Проводит один раунд игры
        self.current_round += 1
        clear()
        print(f"\n{'='*20} РАУНД {self.current_round} {'='*20}")
        
        while True:
            print("\nВаш ход:")
            self.ui.get_dice_roll_input(self.current_round)
            player_roll = self.player.roll_dice()
            
            computer_roll = self.computer.roll_dice()
            
            print(f"Вы бросили кубик: {DICE_SYMBOLS[player_roll]} {player_roll}")
            print(f"Компьютер бросил кубик: {DICE_SYMBOLS[computer_roll]} {computer_roll}")
            
            if player_roll > computer_roll:
                difference = player_roll - computer_roll
                self.player.add_score(difference)
                print(f"Вы выиграли раунд! +{difference} очков")
                return difference, 0, True
                
            elif computer_roll > player_roll:
                difference = computer_roll - player_roll
                self.player.add_score(-difference)
                print(f"Компьютер выиграл раунд! -{difference} очков")
                return -difference, difference, True
                
            else:
                print("Ничья! Перебрасываем кубики...")
                time.sleep(2)
                continue
    
    def display_game_status(self):
        # Отображает текущее состояние игры
        print(f"\nСтатус игры после {self.current_round} раунда(ов) из {self.rounds_total}:")
        print(f"Ваш счет: {self.player.get_score()}")
        print(f"Счет компьютера: {self.computer.get_score()}")
        
        if self.player.get_score() > 0:
            print("Вы впереди! 🏆")
        elif self.player.get_score() < 0:
            print("Компьютер впереди! 🤖")
        else:
            print("Счет равный! ⚖️")
        
        if self.current_round < self.rounds_total:
            self.ui.check_exit_to_menu()
    
    def display_final_results(self):
        # Отображает финальные результаты игры
        print("\n" + "="*60)
        print("                 ИТОГИ ИГРЫ")
        print("="*60)
        
        print(f"Время начала игры: {self.start_time.strftime(DATE_FORMAT)}")
        print(f"Время окончания: {datetime.now().strftime(DATE_FORMAT)}")
        print(f"Игрок: {self.player.get_name()}")
        print(f"Уровень игры: {get_level_name(self.rounds_total)}")
        print(f"Количество раундов: {self.rounds_total}")
        
        print(f"\nФинальный счет:")
        print(f"Ваш счет: {self.player.get_score()}")
        print(f"Счет компьютера: {self.computer.get_score()}")
        
        if self.player.get_score() > 0:
            print(f"\n🎉 ПОЗДРАВЛЯЕМ! ВЫ ПОБЕДИЛИ! 🎉")
            print(f"Вы выиграли с преимуществом в {self.player.get_score()} очков!")
        elif self.player.get_score() < 0:
            print(f"\n😞 Вы проиграли...")
            print(f"Компьютер победил с преимуществом в {abs(self.player.get_score())} очков.")
        else:
            print(f"\n🤝 НИЧЬЯ!")
            print("Вы сыграли наравне с компьютером!")
        
        print("="*60)
    
    def save_game_result(self):
        # Сохраняет результат игры
        self.score_manager.save_result(self.player.get_name(), self.rounds_total, self.player.get_score())
    
    def start(self):
        # Запускает игру
        try:
            self.initialize_game()
            
            for _ in range(self.rounds_total):
                self.play_round()
                self.display_game_status()
            
            clear()
            self.display_final_results()
            self.save_game_result()
            
            input("\nНажмите Enter для возврата в главное меню...")
            
        except ExitToMenuError:
            clear()
            print("\n🔙 Возврат в главное меню...")
            print("Результат игры не сохранен.")
            time.sleep(1)
        except KeyboardInterrupt:
            clear()
            print("\n🔙 Возврат в главное меню...")
            print("Результат игры не сохранен.")
            time.sleep(1)
        except Exception as e:
            print(f"\nПроизошла ошибка во время игры: {e}")
            print("Попробуйте начать игру заново.")
