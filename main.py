# Основной файл игры 
# Управляет меню и запуском игры

from game.game import start_game
from game.score import get_results
from game.exceptions import InvalidInputError, ExitToMenuError
from game.settings import clear


def show_menu():
    # Отображает главное меню игры
    clear()
    print("\n" + "="*50)
    print("           ИГРА 'КОСТИ'")
    print("="*50)
    print("1. Играть")
    print("2. Посмотреть результаты")
    print("3. Выйти")
    print("="*50)


def main():
    # Основная функция программы
    while True:
        try:
            show_menu()
            choice = input("Выберите пункт меню (1-3): ").strip()
            
            if choice == "1":
                clear()
                start_game()
            elif choice == "2":
                clear()
                get_results()
            elif choice == "3":
                clear()
                print("\nСпасибо за игру! До свидания!")
                break
            else:
                raise InvalidInputError("Неверный выбор! Введите число от 1 до 3.")
                
        except InvalidInputError as e:
            print(f"Ошибка: {e}")
        except ExitToMenuError:
            # ExitToMenuError обрабатывается в start_game()
            continue
        except KeyboardInterrupt:
            print("\n\nИгра прервана пользователем. До свидания!")
            break
        except Exception as e:
            print(f"Произошла неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()