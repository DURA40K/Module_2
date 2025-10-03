# Основной файл игры 
# Управляет меню и запуском игры

from game.game import Game
from game.score import ScoreManager
from game.exceptions import InvalidInputError
from game.settings import clear


class GameController:
    # Контроллер приложения - управляет главным меню и запуском компонентов
    
    def __init__(self):
        # Инициализация контроллера
        self.running = True
        self.score_manager = ScoreManager()
    
    def show_menu(self):
        # Отображает главное меню игры
        clear()
        print("\n" + "="*50)
        print("           ИГРА 'КОСТИ'")
        print("="*50)
        print("1. Играть")
        print("2. Посмотреть результаты")
        print("3. Выйти")
        print("="*50)
    
    def get_menu_choice(self):
        # Получает выбор пользователя из главного меню
        choice = input("Выберите пункт меню (1-3): ").strip()
        if choice not in ["1", "2", "3"]:
            raise InvalidInputError("Неверный выбор! Введите число от 1 до 3.")
        return choice
    
    def handle_play_game(self):
        # Обрабатывает выбор "Играть"
        game = Game()
        game.start()
    
    def handle_view_results(self):
        # Обрабатывает выбор "Посмотреть результаты"
        self.score_manager.get_results()
    
    def handle_exit(self):
        # Обрабатывает выбор "Выйти"
        clear()
        print("\nСпасибо за игру! До свидания!")
        self.running = False
    
    def run(self):
        # Основной цикл приложения
        while self.running:
            try:
                self.show_menu()
                choice = self.get_menu_choice()
                
                if choice == "1":
                    self.handle_play_game()
                elif choice == "2":
                    self.handle_view_results()
                elif choice == "3":
                    self.handle_exit()
                    
            except InvalidInputError as e:
                print(f"Ошибка: {e}")
                input("Нажмите Enter для продолжения...")
            except KeyboardInterrupt:
                print("\n\nИгра прервана пользователем. До свидания!")
                self.running = False
            except Exception as e:
                print(f"Произошла неожиданная ошибка: {e}")
                input("Нажмите Enter для продолжения...")


if __name__ == "__main__":
    # Прямой запуск контроллера - чистый ООП подход
    controller = GameController()
    controller.run()