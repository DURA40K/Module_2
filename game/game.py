# Основная логика игры

import time
from datetime import datetime
from .models import Player, Computer
from .settings import GAME_LEVELS, GAME_LEVELS_CONVERT, DICE_SYMBOLS, DATE_FORMAT, clear
from .exceptions import InvalidInputError, InvalidRollError, ExitToMenuError
from .score import save_result


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
            if choice in ['y', 'yes', 'да', 'д']:
                return True
            elif choice in ['n', 'no', 'нет', 'н']:
                return False
            else:
                print("Введите 'y' для подтверждения или 'n' для отмены.")
        except KeyboardInterrupt:
            return True


def check_exit_to_menu():
    # Проверяет, хочет ли пользователь выйти в главное меню
    while True:
        try:
            choice = input("Нажмите Enter для продолжения (1 - выход в меню): ").strip()
            if choice == "":
                clear()
                return
            elif choice == "1":
                if confirm_exit_to_menu():
                    raise ExitToMenuError("Выход в главное меню")
                else:
                    clear()
                    return
            else:
                print("Нажмите Enter для продолжения или '1' для выхода в меню.")
        except KeyboardInterrupt:
            if confirm_exit_to_menu():
                raise ExitToMenuError("Выход в главное меню")


def get_player_name():
    # Получает имя игрока
    while True:
        try:
            clear()
            name = input("\nВведите ваше имя (1 - выход в меню): ").strip()
            if name == '1':
                if confirm_exit_to_menu():
                    raise ExitToMenuError("Выход в главное меню")
                else:
                    continue
            if not name:
                raise InvalidInputError("Имя не может быть пустым!")
            if len(name) > 20:
                raise InvalidInputError("Имя слишком длинное (максимум 20 символов)!")
            return name
        except InvalidInputError as e:
            print(f"Ошибка: {e}")
            input("Нажмите Enter для продолжения...")


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
                if confirm_exit_to_menu():
                    raise ExitToMenuError("Выход в главное меню")
                else:
                    continue
            
            if choice not in GAME_LEVELS:
                raise InvalidInputError("Неверный выбор! Введите число от 1 до 4.")
            
            rounds = GAME_LEVELS[choice]
            level_name = GAME_LEVELS_CONVERT[rounds]
            clear()
            print(f"\nВыбран уровень: {level_name} ({rounds} раундов)")
            input("Нажмите Enter для начала игры...")
            clear()
            return rounds
            
        except InvalidInputError as e:
            print(f"Ошибка: {e}")
            input("Нажмите Enter для продолжения...")


def roll_dice_input(round_number=None):
    # Обрабатывает ввод для броска кубика
    while True:
        try:
            user_input = input("Нажмите Enter для броска кубика (1 - выход в меню): ")
            if user_input == "":
                return True
            elif user_input == "1":
                if confirm_exit_to_menu():
                    raise ExitToMenuError("Выход в главное меню")
                else:
                    clear()
                    if round_number:
                        print(f"\n{'='*20} РАУНД {round_number} {'='*20}")
                        print("\nВаш ход:")
                    continue
            else:
                print("Бросок не сделан!!! Нажмите \"Enter\" для повторного броска или '1' для выхода.")
        except KeyboardInterrupt:
            if confirm_exit_to_menu():
                raise ExitToMenuError("Выход в главное меню")


def play_round(player, computer, round_number):
    # Проводит один раунд игры
    clear()
    print(f"\n{'='*20} РАУНД {round_number} {'='*20}")
    
    while True:
        print("\nВаш ход:")
        roll_dice_input(round_number)
        player_roll = player.roll_dice()
        
        computer_roll = computer.roll_dice()
        
        print(f"Вы бросили кубик: {DICE_SYMBOLS[player_roll]} {player_roll}")
        print(f"Компьютер бросил кубик: {DICE_SYMBOLS[computer_roll]} {computer_roll}")
        
        if player_roll > computer_roll:
            difference = player_roll - computer_roll
            player.add_score(difference)
            print(f"Вы выиграли раунд! +{difference} очков")
            return difference, 0, True
            
        elif computer_roll > player_roll:
            difference = computer_roll - player_roll
            player.add_score(-difference)
            print(f"Компьютер выиграл раунд! -{difference} очков")
            return -difference, difference, True
            
        else:
            print("Ничья! Перебрасываем кубики...")
            time.sleep(2)
            continue


def display_game_status(player, computer, round_number, total_rounds):
    # Отображает текущее состояние игры
    print(f"\nСтатус игры после {round_number} раунда(ов) из {total_rounds}:")
    print(f"Ваш счет: {player.get_score()}")
    print(f"Счет компьютера: {computer.get_score()}")
    
    if player.get_score() > 0:
        print("Вы впереди! 🏆")
    elif player.get_score() < 0:
        print("Компьютер впереди! 🤖")
    else:
        print("Счет равный! ⚖️")
    
    if round_number < total_rounds:
        check_exit_to_menu()


def display_final_results(player, computer, rounds, start_time):
    # Отображает финальные результаты игры
    print("\n" + "="*60)
    print("                 ИТОГИ ИГРЫ")
    print("="*60)
    
    print(f"Время начала игры: {start_time.strftime(DATE_FORMAT)}")
    print(f"Время окончания: {datetime.now().strftime(DATE_FORMAT)}")
    print(f"Игрок: {player.get_name()}")
    print(f"Уровень игры: {GAME_LEVELS_CONVERT[rounds]}")
    print(f"Количество раундов: {rounds}")
    
    print(f"\nФинальный счет:")
    print(f"Ваш счет: {player.get_score()}")
    print(f"Счет компьютера: {computer.get_score()}")
    
    if player.get_score() > 0:
        print(f"\n🎉 ПОЗДРАВЛЯЕМ! ВЫ ПОБЕДИЛИ! 🎉")
        print(f"Вы выиграли с преимуществом в {player.get_score()} очков!")
    elif player.get_score() < 0:
        print(f"\n😞 Вы проиграли...")
        print(f"Компьютер победил с преимуществом в {abs(player.get_score())} очков.")
    else:
        print(f"\n🤝 НИЧЬЯ!")
        print("Вы сыграли наравне с компьютером!")
    
    print("="*60)


def start_game():
    # Запускает игру
    try:
        print("\n🎲 Добро пожаловать в игру 'КОСТИ'! 🎲")
        print("Вам предстоит сразиться с компьютером в броске кубиков!")
        
        player_name = get_player_name()
        rounds = get_game_level()
        
        player = Player(player_name)
        computer = Computer()
        
        start_time = datetime.now()
        
        print(f"\n🎮 Игра начинается! Удачи, {player_name}!")
        time.sleep(1)
        
        for round_num in range(1, rounds + 1):
            play_round(player, computer, round_num)
            display_game_status(player, computer, round_num, rounds)
        
        clear()
        display_final_results(player, computer, rounds, start_time)
        
        save_result(player.get_name(), rounds, player.get_score())
        
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
