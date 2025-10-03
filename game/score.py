# Модуль для работы с результатами игры
# Класс ScoreManager для сохранения и чтения результатов

import json
from datetime import datetime
from .settings import RESULTS_FILE, DATE_FORMAT, clear, get_level_name


class ScoreManager:
    # Класс для управления результатами игры
    
    def __init__(self, results_file=RESULTS_FILE):
        # Инициализация менеджера результатов
        self.results_file = results_file
    
    def save_result(self, name, rounds, score):
        # Сохраняет результат игры в файл
        result = {
            "Дата": datetime.now().strftime(DATE_FORMAT),
            "Игрок": name,
            "Уровень игры": get_level_name(rounds),
            "Количество раундов": rounds,
            "Итоговый счет": score
        }
        
        results = self._load_results()
        results.append(result)
        self._save_results(results)
        print(f"\nРезультат игры сохранен в файл {self.results_file}")
    
    def _load_results(self):
        # Загружает результаты из файла
        try:
            with open(self.results_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_results(self, results):
        # Сохраняет результаты в файл
        try:
            with open(self.results_file, 'w', encoding='utf-8') as file:
                json.dump(results, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении результата: {e}")
    
    def get_results(self):
        # Читает и выводит все сохраненные результаты с пагинацией
        clear()
        results = self._load_results()
        
        if not results:
            print("\nРезультатов игр пока нет.")
            print("Сыграйте несколько игр, чтобы увидеть статистику!")
            input("\nНажмите Enter для возврата в главное меню...")
            return
        
        # Сортируем результаты по дате (новые сверху)
        results.sort(key=lambda x: x.get('Дата', ''), reverse=True)
        
        page = 0
        per_page = 8
        total_pages = self._calculate_total_pages(len(results), per_page)
        
        while True:
            self._display_page(results, page, per_page, total_pages)
            self._show_statistics(results)
            action = self._get_navigation_choice(page, total_pages)
            
            if action == "previous":
                page -= 1
            elif action == "next":
                page += 1
            elif action == "exit":
                break
            else:
                print("❌ Неверный выбор.")
                input("Нажмите Enter для продолжения...")
    
    def _calculate_total_pages(self, total_results, per_page):
        # Вычисляет общее количество страниц
        return (total_results + per_page - 1) // per_page
    
    def _display_result(self, result, index):
        # Отображает один результат игры
        score = result.get('Итоговый счет', 0)
        score_text = f"+{score}" if score > 0 else str(score)
        status = "🏆" if score > 0 else "😞" if score < 0 else "🤝"
        
        date = result.get('Дата', 'Неизвестно')[:16]
        player = result.get('Игрок', 'Неизвестно')[:15]
        level = result.get('Уровень игры', 'Неизвестно')[:6]
        
        print(f"{index:2}. {date} | {player:15} | {level:6} | {score_text:4} {status}")
    
    def _display_page(self, results, page, per_page, total_pages):
        # Отображает одну страницу результатов
        clear()
        start = page * per_page
        end = start + per_page
        current_results = results[start:end]
        
        print("\n" + "="*70)
        print("                     РЕЗУЛЬТАТЫ ИГР")
        print("="*70)
        print(f"Страница {page + 1} из {total_pages} | Результаты {start + 1}-{min(end, len(results))} из {len(results)}")
        print("-" * 70)
        print("№   Дата и время     | Игрок           | Уровень | Счет")
        print("-" * 70)
        
        for i, result in enumerate(current_results, start + 1):
            self._display_result(result, i)
    
    def _get_navigation_choice(self, page, total_pages):
        # Получает выбор навигации и возвращает действие
        options = []
        if page > 0:
            options.append("(1) Предыдущая страница")
        if page < total_pages - 1:
            options.append(f"({2 if page > 0 else 1}) Следующая страница")
        options.append(f"({len(options) + 1}) Выйти в меню")
        
        print("\nНавигация:")
        for option in options:
            print(option)
        
        choice = input("Выберите действие: ").strip()
        
        if page > 0 and choice == '1':
            return "previous"
        elif page < total_pages - 1 and choice == ('2' if page > 0 else '1'):
            return "next"
        elif choice == str(len(options)):
            return "exit"
        else:
            return "invalid"
    
    def _show_statistics(self, results):
        # Показывает общую статистику
        wins = len([r for r in results if r.get('Итоговый счет', 0) > 0])
        losses = len([r for r in results if r.get('Итоговый счет', 0) < 0])
        draws = len([r for r in results if r.get('Итоговый счет', 0) == 0])
        
        win_rate = (wins / len(results)) * 100 if len(results) > 0 else 0
        
        print("-" * 70)
        print(f"Всего: {len(results)} | Побед: {wins} | Поражений: {losses} | Ничьих: {draws} | Процент побед: {win_rate:.1f}%")
        print("="*70)