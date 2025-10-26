# custom_sql_views.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import psycopg2
from psycopg2 import extras

# Використовуємо налаштування з queries.py
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'tour_agency',
    'user': 'postgres',
    'password': 'lkol2567',
}


def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print('Помилка підключення до БД:', e)
        return None


def show_custom_sql_window():
    sql_win = tk.Toplevel()
    sql_win.title("Виконати SQL запит")
    sql_win.geometry("900x700")
    sql_win.transient()
    sql_win.grab_set()

    # Основний контейнер
    main_frame = ttk.Frame(sql_win)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Заголовок
    ttk.Label(main_frame, text="Введіть SQL запит:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))

    # Текстове поле для SQL
    sql_text = scrolledtext.ScrolledText(main_frame, height=8, width=80, font=('Consolas', 11))
    sql_text.pack(fill='x', pady=(0, 10))
    sql_text.focus_set()

    # Кнопки виконання
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill='x', pady=(0, 10))

    def execute_query():
        query = sql_text.get('1.0', tk.END).strip()
        if not query:
            messagebox.showwarning("Попередження", "Будь ласка, введіть SQL запит")
            return

        try:
            conn = get_db_connection()
            if not conn:
                messagebox.showerror("Помилка", "Не вдалося підключитися до бази даних")
                return

            cursor = conn.cursor()

            # Визначаємо тип запиту
            query_upper = query.upper().strip()
            is_select = query_upper.startswith('SELECT')
            is_show = query_upper.startswith('SHOW')
            is_describe = query_upper.startswith('DESCRIBE') or query_upper.startswith('\\D')
            is_pragma = query_upper.startswith('PRAGMA')

            if is_select or is_show or is_describe or is_pragma:
                # Для SELECT та інших запитів, що повертають результати
                cursor.execute(query)

                # Отримуємо результати тільки якщо є дані
                try:
                    results = cursor.fetchall()
                    column_names = [description[0] for description in cursor.description]
                except psycopg2.ProgrammingError:
                    # Якщо немає результатів (наприклад, для DDL команд)
                    results = []
                    column_names = []

                # Очищаємо попередні результати
                for widget in results_frame.winfo_children():
                    widget.destroy()

                if results and column_names:
                    # Створюємо Treeview для відображення результатів
                    tree_frame = ttk.Frame(results_frame)
                    tree_frame.pack(fill='both', expand=True)

                    # Додаємо прокрутку
                    tree_scroll_y = ttk.Scrollbar(tree_frame)
                    tree_scroll_y.pack(side='right', fill='y')

                    tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
                    tree_scroll_x.pack(side='bottom', fill='x')

                    tree = ttk.Treeview(tree_frame,
                                        columns=column_names,
                                        show='headings',
                                        yscrollcommand=tree_scroll_y.set,
                                        xscrollcommand=tree_scroll_x.set)

                    # Налаштовуємо заголовки
                    for col in column_names:
                        tree.heading(col, text=col)
                        tree.column(col, width=100, minwidth=50)

                    # Додаємо дані
                    for row in results:
                        tree.insert('', 'end', values=row)

                    tree.pack(fill='both', expand=True)

                    # Налаштовуємо прокрутку
                    tree_scroll_y.config(command=tree.yview)
                    tree_scroll_x.config(command=tree.xview)

                    # Інформація про результати
                    info_label.config(text=f"Знайдено записів: {len(results)}")
                else:
                    info_label.config(text="Запит виконано успішно. Результатів не знайдено.")

            else:
                # Для інших запитів (INSERT, UPDATE, DELETE, CREATE, etc.)
                cursor.execute(query)
                conn.commit()
                affected_rows = cursor.rowcount
                info_label.config(text=f"Запит виконано успішно. Змінено записів: {affected_rows}")

            conn.close()

        except psycopg2.Error as e:
            error_message = f"Помилка виконання запиту:\n{str(e)}"
            messagebox.showerror("Помилка", error_message)
            info_label.config(text="Помилка виконання запиту")
        except Exception as e:
            error_message = f"Неочікувана помилка:\n{str(e)}"
            messagebox.showerror("Помилка", error_message)
            info_label.config(text="Помилка виконання запиту")

    def clear_query():
        sql_text.delete('1.0', tk.END)
        # Очищаємо результати
        for widget in results_frame.winfo_children():
            widget.destroy()
        info_label.config(text="")

    ttk.Button(button_frame, text="Виконати запит", command=execute_query).pack(side='left', padx=(0, 10))
    ttk.Button(button_frame, text="Очистити", command=clear_query).pack(side='left')

    # Інформаційний label
    info_label = ttk.Label(main_frame, text="", font=('Arial', 10))
    info_label.pack(anchor='w', pady=(0, 10))

    # Область для результатів
    ttk.Label(main_frame, text="Результати:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 5))

    results_frame = ttk.Frame(main_frame)
    results_frame.pack(fill='both', expand=True)

    # Приклади запитів
    examples_frame = ttk.LabelFrame(main_frame, text="Приклади запитів")
    examples_frame.pack(fill='x', pady=(11, 0))

    examples = [
        "SELECT * FROM tourist LIMIT 10",
        "SELECT full_name, passport FROM tourist WHERE age > 30",
        "UPDATE tourist SET children_info = 'немає' WHERE id = 86",
        "DELETE FROM tourist WHERE id = 1"
    ]

    def insert_example(example):
        sql_text.delete('1.0', tk.END)
        sql_text.insert('1.0', example)

    for example in examples:
        example_btn = ttk.Button(examples_frame, text=example,
                                 command=lambda ex=example: insert_example(ex))
        example_btn.pack(fill='x', pady=2)

    # Обробка клавіш
    def on_key_press(event):
        if event.state & 0x4 and event.keysym == 'Return':  # Ctrl+Enter
            execute_query()
        elif event.keysym == 'Escape':
            sql_win.destroy()

    sql_text.bind('<KeyPress>', on_key_press)
    sql_win.bind('<KeyPress>', on_key_press)

    # Інформація про гарячі клавіші
    help_label = ttk.Label(main_frame, text="Ctrl+Enter - виконати запит, Escape - закрити вікно",
                           font=('Arial', 9), foreground='gray')
    help_label.pack(anchor='center', pady=(5, 0))