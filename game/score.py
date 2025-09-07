# Модуль для работы с результатами игры
# Сохранение и чтение результатов из файла

import json
from datetime import datetime
from .settings import RESULTS_FILE, DATE_FORMAT, GAME_LEVELS_CONVERT, clear


def save_result(name, rounds, score):
    # Сохраняет результат игры в файл
    result = {
        "Дата": datetime.now().strftime(DATE_FORMAT),
        "Игрок": name,
        "Уровень игры": GAME_LEVELS_CONVERT.get(rounds, "Неизвестный"),
        "Количество раундов": rounds,
        "Итоговый счет": score
    }
    
    results = []
    try:
        with open(RESULTS_FILE, 'r', encoding='utf-8') as file:
            results = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        results = []
    
    results.append(result)
    
    try:
        with open(RESULTS_FILE, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=2)
        print(f"\nРезультат игры сохранен в файл {RESULTS_FILE}")
    except Exception as e:
        print(f"Ошибка при сохранении результата: {e}")


def get_results():
    # Читает и выводит все сохраненные результаты с пагинацией
    clear()
    try:
        with open(RESULTS_FILE, 'r', encoding='utf-8') as file:
            results = json.load(file)
    except FileNotFoundError:
        print("\nРезультатов игр пока нет.")
        print("Сыграйте несколько игр, чтобы увидеть статистику!")
        input("\nНажмите Enter для возврата в главное меню...")
        return
    except json.JSONDecodeError:
        print("\nОшибка при чтении файла результатов.")
        input("\nНажмите Enter для возврата в главное меню...")
        return
    
    if not results:
        print("\nРезультатов игр пока нет.")
        input("\nНажмите Enter для возврата в главное меню...")
        return
        
    # Сортируем результаты по дате (новые сверху)
    results.sort(key=lambda x: x.get('Дата', ''), reverse=True)
    
    page = 0
    per_page = 8  # Увеличиваем до 8 результатов на страницу (компактный формат)
    total_pages = calculate_total_pages(len(results), per_page)
    
    while True:
        display_page(results, page, per_page, total_pages)
        show_statistics(results)
        action = get_navigation_choice(page, total_pages)
        
        if action == "previous":
            page -= 1
        elif action == "next":
            page += 1
        elif action == "exit":
            break
        else:
            print("❌ Неверный выбор.")
            input("Нажмите Enter для продолжения...")


def calculate_total_pages(total_results, per_page):
    # Вычисляет общее количество страниц
    return (total_results + per_page - 1) // per_page


def display_result(result, index):
    # Отображает один результат игры
    score = result.get('Итоговый счет', 0)
    score_text = f"+{score}" if score > 0 else str(score)
    status = "🏆" if score > 0 else "😞" if score < 0 else "🤝"
    
    date = result.get('Дата', 'Неизвестно')[:16]
    player = result.get('Игрок', 'Неизвестно')[:15]
    level = result.get('Уровень игры', 'Неизвестно')[:6]
    
    print(f"{index:2}. {date} | {player:15} | {level:6} | {score_text:4} {status}")


def display_page(results, page, per_page, total_pages):
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
        display_result(result, i)


def get_navigation_choice(page, total_pages):
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


def show_statistics(results):
    # Показывает общую статистику
    wins = len([r for r in results if r.get('Итоговый счет', 0) > 0])
    losses = len([r for r in results if r.get('Итоговый счет', 0) < 0])
    draws = len([r for r in results if r.get('Итоговый счет', 0) == 0])
    
    win_rate = (wins / len(results)) * 100 if len(results) > 0 else 0
    
    print("-" * 70)
    print(f"Всего: {len(results)} | Побед: {wins} | Поражений: {losses} | Ничьих: {draws} | Процент побед: {win_rate:.1f}%")
    print("="*70)
