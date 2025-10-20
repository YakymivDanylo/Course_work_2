import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from models.current_user import current_user
import queries as db

def show_queries_window():
    win = tk.Toplevel()
    win.title('Функціональні запити')

    def save_result(result, query_name):
        if current_user['role'] in ['Авторизований', 'Оператор', 'Адміністратор']:
            try:
                filename = f"результат_{query_name}_{current_user['login']}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Запит: {query_name}\n")
                    f.write(f"Користувач: {current_user['login']}\n")
                    f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("Результат:\n")
                    f.write(str(result))
                messagebox.showinfo('Успіх', f'Результат збережено у файл {filename}')
            except Exception as e:
                messagebox.showerror('Помилка', f'Не вдалося зберегти: {e}')
        else:
            messagebox.showwarning('Доступ заборонено', 'Тільки авторизовані користувачі можуть зберігати результати')

    if current_user['role'] == 'Гість':
        def show_basic_info():
            messagebox.showinfo('Інформація',
                                'Для гостей доступна тільки базова інформація. Подайте заявку на підвищення прав для повного доступу.')

        tk.Button(win, text='Базова інформація', command=show_basic_info).pack(fill='x')
        return

    def display_table(title, columns, data, query_name=None, raw_result=None):
        table_win = tk.Toplevel()
        table_win.title(title)

        tree = ttk.Treeview(table_win, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center')
        tree.pack(fill='both', expand=True)

        for row in data:
            tree.insert('', 'end', values=row)

        def on_close():
            if current_user['role'] in ['Авторизований', 'Оператор',
                                        'Адміністратор'] and query_name and raw_result is not None:
                if messagebox.askyesno('Збереження', 'Зберегти результат?'):
                    save_result(raw_result, query_name)
            table_win.destroy()

        table_win.protocol("WM_DELETE_WINDOW", on_close)

        tk.Button(table_win, text='Закрити', command=on_close).pack(pady=5)

    if current_user['role'] in ['Оператор', 'Адміністратор']:
        def show_profitability():
            res = db.get_profitability()
            if res is not None:
                data = [(f"Рентабельність", f"{res:.2f}")]
            else:
                data = [("Результат", "Даних немає")]
            display_table(
                'Рентабельність',
                ('Показник', 'Значення'),
                data,
                query_name='Рентабельність',
                raw_result=res
            )

        tk.Button(win, text='Рентабельність представництва', command=show_profitability).pack(fill='x')

    def show_financial_by_period():
        form = tk.Toplevel()
        form.title('Витрати/прибутки за період')
        tk.Label(form, text='З').grid(row=0, column=0)
        date_from = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_from.grid(row=0, column=1)
        tk.Label(form, text='По').grid(row=1, column=0)
        date_to = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_to.grid(row=1, column=1)

        def run():
            FIELD_NAMES = {
                'id': 'ID',
                'group_id': 'ID групи',
                'income': 'Дохід(грн.)',
                'profit': 'Прибуток(грн.)',
                'expense_hotel': 'Витрати на готель(грн.)',
                'expense_transport': 'Витрати на транспорт(грн.)',
                'expense_excursion': 'Витрати на екскурсії(грн.)',
                'expense_equipment': 'Витрати на спорядження(грн.)',
                'expense_cargo': 'Витрати на вантаж(грн.)',
                'expense_airport': 'Витрати на аеропорт(грн.)'
            }

            res = db.get_financial_by_period(date_from.get(), date_to.get())
            if res:
                original_columns = list(res[0].keys())
                columns_to_display = [col for col in original_columns if col != 'id']
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]
                data = [tuple(item[col] for col in columns_to_display) for item in res]
            else:
                display_columns = []
                data = []

            display_table('Витрати/прибутки за період', display_columns, data,
                          query_name='Витрати/прибутки за період', raw_result=res)

        tk.Button(form, text='Показати', command=run).grid(row=2, column=0, columnspan=2)

    tk.Button(win, text='Витрати/прибутки за період', command=show_financial_by_period).pack(fill='x')

    def show_flight_load():
        form = tk.Toplevel()
        form.title('Завантаження рейсу')
        tk.Label(form, text='Дата').grid(row=0, column=0)
        date = DateEntry(form, date_pattern='yyyy-mm-dd')
        date.grid(row=0, column=1)

        def run():
            FIELD_NAMES = {
                'id': 'ID',
                'flight_number': 'Номер рейсу',
                'date': 'Дата',
                'seats_count': 'Загальна кількість місць',
                'free_seats': 'Вільні місця',
                'cargo_weight': 'Вага вантажу (кг)',
                'plane_class': 'Клас літака',
                'occupied_seats': 'Зайняті місця',
                'load_percentage': 'Завантаження (%)'
            }

            res = db.get_flight_load_by_date(date.get())
            if res:
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []
                display_columns = [FIELD_NAMES.get(col, col) for col in original_columns]
                data = [tuple(item[col] for col in original_columns) for item in res] if original_columns else []
            else:
                display_columns = []
                data = []

            display_table('Завантаження рейсу', display_columns, data, query_name='Завантаження_рейсу', raw_result=res)

        tk.Button(form, text='Показати', command=run).grid(row=1, column=0, columnspan=2)

    tk.Button(win, text='Завантаження рейсу на дату', command=show_flight_load).pack(fill='x')

    def show_excursion_stats():
        form = tk.Toplevel()
        form.title('Статистика екскурсій')
        tk.Label(form, text='З').grid(row=0, column=0)
        date_from = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_from.grid(row=0, column=1)
        tk.Label(form, text='По').grid(row=1, column=0)
        date_to = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_to.grid(row=1, column=1)

        def run():
            FIELD_NAMES = {
                'tourists_count': 'Кількість туристів',
                'excursion_name': 'Назва екскурсії',
                'agency_name': 'Назва агенції',
                'excursion_orders': 'Кількість замовлень',
                'id': 'ID',
                'date': 'Дата',
                'price': 'Ціна',
                'duration': 'Тривалість',
                'guide_name': 'Ім\'я гіда',
                'location': 'Місце проведення'
            }

            res = db.get_excursion_stats(date_from.get(), date_to.get())
            if res:
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []
                display_columns = [FIELD_NAMES.get(col, col) for col in original_columns]
                data = [tuple(item[col] for col in original_columns) for item in res] if original_columns else []
            else:
                display_columns = []
                data = []

            display_table('Статистика екскурсій', display_columns, data)

        tk.Button(form, text='Показати', command=run).grid(row=2, column=0, columnspan=2)

    tk.Button(win, text='Статистика екскурсій за період', command=show_excursion_stats).pack(fill='x')

    def show_cargo_stats():
        form = tk.Toplevel()
        form.title('Вантажообіг')
        tk.Label(form, text='З').grid(row=0, column=0)
        date_from = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_from.grid(row=0, column=1)
        tk.Label(form, text='По').grid(row=1, column=0)
        date_to = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_to.grid(row=1, column=1)

        def run():
            FIELD_NAMES = {
                'places_count': 'Кількість місць',
                'total_weight': 'Загальна вага (кг)',
                'flights_count': 'Кількість рейсів',
                'plane_class': 'Клас літака',
                'id': 'ID',
                'date': 'Дата',
                'flight_number': 'Номер рейсу',
                'cargo_type': 'Тип вантажу',
                'average_weight': 'Середня вага',
                'max_weight': 'Максимальна вага',
                'min_weight': 'Мінімальна вага'
            }

            res = db.get_cargo_stats(date_from.get(), date_to.get())
            if res:
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []
                display_columns = [FIELD_NAMES.get(col, col) for col in original_columns]
                data = [tuple(item[col] for col in original_columns) for item in res] if original_columns else []
            else:
                display_columns = []
                data = []

            display_table('Вантажообіг', display_columns, data, query_name='Вантажообіг', raw_result=res)

        tk.Button(form, text='Показати', command=run).grid(row=2, column=0, columnspan=2)

    tk.Button(win, text='Вантажообіг за період', command=show_cargo_stats).pack(fill='x')

    def show_tourist_info():
        form = tk.Toplevel()
        form.title('Інформація про туриста')
        tourists = db.get_tourists()
        combo = ttk.Combobox(form, values=[t['full_name'] for t in tourists])
        combo.grid(row=0, column=1)
        tk.Label(form, text='Турист').grid(row=0, column=0)

        def run():
            tourist_id = tourists[combo.current()]['id'] if combo.current() >= 0 else None
            res = db.get_tourist_info(tourist_id)
            if res:
                columns = ['Характеристика', 'Значення']
                data = [
                    ('ID', res['id']),
                    ('ПІБ', res['full_name']),
                    ('Паспорт', res['passport']),
                    ('Стать', res['gender']),
                    ('Вік', res['age']),
                    ('Категорія', res['category']),
                    ('Діти', res['children_info']),
                    ('Кількість поїздок', res['trips_count']),
                    ('Дати прибуття', ', '.join(str(d) for d in res['arrivals']) if res['arrivals'] else 'Немає даних'),
                    ('Дати відбуття', ', '.join(str(d) for d in res['departures']) if res['departures'] else 'Немає даних'),
                    ('Готелі', ', '.join(res['hotels']) if res['hotels'] else 'Немає даних'),
                    ('Екскурсії', ', '.join(res['excursions']) if res['excursions'] else 'Немає даних'),
                    ('Вантаж', ', '.join(str(c) for c in res['cargos']) if res['cargos'] else 'Немає даних')
                ]
            else:
                columns = ['Інформація']
                data = [('Дані не знайдено',)]
            display_table('Інформація про туриста', columns, data, query_name='Інформація про туриста', raw_result=res)

        tk.Button(form, text='Показати', command=run).grid(row=1, column=0, columnspan=2)

    tk.Button(win, text='Інформація про туриста', command=show_tourist_info).pack(fill='x')

    def show_group_financial():
        form = tk.Toplevel()
        form.title('Фінансовий звіт групи')
        groups = db.get_tourist_groups()
        combo = ttk.Combobox(form, values=[g['group_identifier'] for g in groups])
        combo.grid(row=0, column=1)
        tk.Label(form, text='Група').grid(row=0, column=0)

        def run():
            FIELD_NAMES = {
                'id': 'ID',
                'group_id': 'ID групи',
                'income': 'Дохід',
                'profit': 'Прибуток',
                'expense_hotel': 'Витрати на готель',
                'expense_transport': 'Витрати на транспорт',
                'expense_excursion': 'Витрати на екскурсії',
                'expense_equipment': 'Витрати на спорядження',
                'expense_cargo': 'Витрати на вантаж',
                'expense_airport': 'Витрати на аеропорт',
                'total_income': 'Загальний дохід',
                'total_expenses': 'Загальні витрати',
                'group_identifier': 'Ідентифікатор групи',
                'tourists_count': 'Кількість туристів',
                'start_date': 'Дата початку',
                'end_date': 'Дата завершення'
            }

            group_id = groups[combo.current()]['id'] if combo.current() >= 0 else None
            res = db.get_group_financial_report(group_id)
            if res:
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []
                columns_to_display = [col for col in original_columns if col != 'id']
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]
                data = [tuple(item[col] for col in columns_to_display) for item in res] if columns_to_display else []
            else:
                display_columns = []
                data = []

            display_table('Фінансовий звіт групи', display_columns, data, query_name='Фінансовий звіт групи',
                          raw_result=res)

        tk.Button(form, text='Показати', command=run).grid(row=1, column=0, columnspan=2)

    tk.Button(win, text='Фінансовий звіт для групи', command=show_group_financial).pack(fill='x')

    def show_hotel_occupancy():
        form = tk.Toplevel()
        form.title('Зайнятість готелів')
        tk.Label(form, text='З').grid(row=0, column=0)
        date_from = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_from.grid(row=0, column=1)
        tk.Label(form, text='По').grid(row=1, column=0)
        date_to = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_to.grid(row=1, column=1)

        def run():
            FIELD_NAMES = {
                'name': 'Назва готелю',
                'tourists_count': 'Кількість туристів',
                'rooms_occupied': 'Зайнято кімнат',
            }

            res = db.get_hotel_occupancy(date_from.get(), date_to.get())
            if res:
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []
                columns_to_display = [col for col in original_columns if col != 'id']
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]
                data = [tuple(item[col] for col in columns_to_display) for item in res] if columns_to_display else []
            else:
                display_columns = []
                data = []

            display_table('Зайнятість готелів', display_columns, data, query_name='Зайнятість готелів', raw_result=res)

        tk.Button(form, text='Показати', command=run).grid(row=2, column=0, columnspan=2)

    tk.Button(win, text='Зайнятість готелів за період', command=show_hotel_occupancy).pack(fill='x')

    def show_customs_tourists():
        form = tk.Toplevel()
        form.title('Туристи для митниці')
        tk.Label(form, text='Категорія').grid(row=0, column=0)
        combo = ttk.Combobox(form, values=['', 'відпочинок', 'вантаж'])
        combo.grid(row=0, column=1)

        def run():
            FIELD_NAMES = {
                'id': 'ID',
                'full_name': 'ПІБ',
                'passport': 'Паспорт',
                'gender': 'Стать',
                'age': 'Вік',
                'category': 'Категорія',
                'children_info': 'Інформація про дітей',
                'nationality': 'Національність',
                'birth_date': 'Дата народження',
                'visa_info': 'Візова інформація',
                'flight_number': 'Номер рейсу',
                'arrival_date': 'Дата прибуття',
                'departure_date': 'Дата відбуття',
                'cargo_weight': 'Вага вантажу',
                'cargo_type': 'Тип вантажу'
            }

            cat = combo.get() if combo.get() else None
            res = db.get_customs_tourists(cat)
            if res:
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []
                columns_to_display = [col for col in original_columns if col != 'id']
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]
                data = [tuple(item[col] for col in columns_to_display) for item in res] if columns_to_display else []
            else:
                display_columns = []
                data = []

            display_table('Туристи для митниці', display_columns, data, query_name='Туристи для митниці',
                          raw_result=res)

        tk.Button(form, text='Показати', command=run).grid(row=1, column=0, columnspan=2)

    tk.Button(win, text='Туристи для митниці', command=show_customs_tourists).pack(fill='x')

    def show_tourists_by_period():
        form = tk.Toplevel()
        form.title('Туристи за період')
        tk.Label(form, text='З').grid(row=0, column=0)
        date_from = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_from.grid(row=0, column=1)
        tk.Label(form, text='По').grid(row=1, column=0)
        date_to = DateEntry(form, date_pattern='yyyy-mm-dd')
        date_to.grid(row=1, column=1)
        tk.Label(form, text='Категорія').grid(row=2, column=0)
        combo = ttk.Combobox(form, values=['', 'відпочинок', 'вантаж'])
        combo.grid(row=2, column=1)

        def run():
            FIELD_NAMES = {
                'id': 'ID',
                'full_name': 'ПІБ',
                'passport': 'Паспорт',
                'gender': 'Стать',
                'age': 'Вік',
                'category': 'Категорія',
                'children_info': 'Інформація про дітей',
                'nationality': 'Національність',
                'birth_date': 'Дата народження',
                'arrival_date': 'Дата прибуття',
                'departure_date': 'Дата відбуття',
                'flight_number': 'Номер рейсу',
                'hotel_name': 'Назва готелю',
                'group_identifier': 'Ідентифікатор групи',
                'trips_count': 'Кількість поїздок',
                'cargo_weight': 'Вага вантажу',
                'cargo_type': 'Тип вантажу'
            }

            cat = combo.get() if combo.get() else None
            res = db.get_tourists_by_period(date_from.get(), date_to.get(), cat)
            if res:
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []
                columns_to_display = [col for col in original_columns if col != 'id']
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]
                data = [tuple(item[col] for col in columns_to_display) for item in res] if columns_to_display else []
            else:
                display_columns = []
                data = []

            display_table('Туристи за період', display_columns, data, query_name='Туристи за період', raw_result=res)

        tk.Button(form, text='Показати', command=run).grid(row=3, column=0, columnspan=2)

    tk.Button(win, text='Список туристів за період', command=show_tourists_by_period).pack(fill='x')