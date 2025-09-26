import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import queries as db
from datetime import datetime
import re
import hashlib

current_user = None

# --- Авторизація ---
def show_login_window():
    def login():
        global current_user
        login_val = entry_login.get()
        password_val = entry_password.get()

        # Додати перевірку на порожні поля
        if not login_val or not password_val:
            messagebox.showerror('Помилка', 'Будь ласка, заповніть всі поля')
            return

        user = db.get_user_by_login(login_val)
        hashed_entered_password = hashlib.sha256(password_val.encode('utf-8')).hexdigest()

        # Додатковий вивід для дебагінга
        print(f"Login attempt: {login_val}")
        print(f"Entered password hash: {hashed_entered_password}")
        if user:
            print(f"Stored password hash: {user['password']}")

        if user and user['password'] == hashed_entered_password:
            current_user = user
            login_win.destroy()
            show_main_menu()
        else:
            messagebox.showerror('Помилка', 'Невірний логін або пароль')

    def forgot_password():
        login_val = entry_login.get()
        user = db.get_user_by_login(login_val)
        if user and current_user and current_user['role'] == 'Адміністратор':
            messagebox.showinfo('Пароль', f"Пароль: {user['password']}")
        else:
            messagebox.showerror('Доступ заборонено', 'Тільки адміністратор може переглядати паролі')

    login_win = tk.Tk()
    login_win.title('Авторизація')
    login_win.attributes('-fullscreen', True)

    frame = tk.Frame(login_win, padx=50, pady=50)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    label_font = ('Arial', 16)
    entry_font = ('Arial', 14)
    btn_font = ('Arial', 14)

    tk.Label(frame, text='Логін', font=label_font).grid(row=0, column=0, sticky='e', pady=10)
    tk.Label(frame, text='Пароль', font=label_font).grid(row=1, column=0, sticky='e', pady=10)

    entry_login = tk.Entry(frame, font=entry_font, width=30)
    entry_password = tk.Entry(frame, show='*', font=entry_font, width=30)
    entry_login.grid(row=0, column=1, pady=10)
    entry_password.grid(row=1, column=1, pady=10)

    tk.Button(frame, text='Увійти', command=login, font=btn_font, width=20).grid(row=2, column=0, columnspan=2, pady=15)
    tk.Button(frame, text='Forgot Password', command=forgot_password, font=btn_font, width=20).grid(row=3, column=0,
                                                                                                    columnspan=2)

    def on_key_press(event):
        if event.keysym == 'Return':
            login()
        elif event.keysym == 'Escape':
            login_win.destroy()
        elif event.keysym == 'F1':
            messagebox.showinfo('Довідка',
                                'Клавішні комбінації:\n'
                                'Enter - Увійти\n'
                                'Escape - Вийти\n'
                                'F1 - Довідка\n'
                                'Tab - Перехід між поля')

    login_win.bind('<KeyPress>', on_key_press)
    entry_login.focus_set()
    login_win.mainloop()

# --- Головне меню ---
def show_main_menu():
    main_win = tk.Tk()
    main_win.title('Головне меню')
    main_win.attributes('-fullscreen', True)

    # Головний контейнер
    main_container = tk.Frame(main_win)
    main_container.pack(expand=True, fill='both')

    canvas = tk.Canvas(main_container)
    scrollbar = tk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    # Створюємо вікно в canvas для scrollable_frame
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    # Функція для оновлення ширини scrollable_frame при зміні розміру canvas
    def configure_scrollable_frame(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind('<Configure>', configure_scrollable_frame)

    welcome_font = ('Arial', 18, 'bold')
    btn_font = ('Arial', 14)

    # Створюємо фрейм для центрування вмісту всередині scrollable_frame
    center_frame = tk.Frame(scrollable_frame)
    center_frame.pack(expand=True, fill='both')

    tk.Label(center_frame, text=f"Вітаємо, {current_user['login']} ({current_user['role']})", font=welcome_font).pack(
        pady=(0, 20))

    def create_button(text, command):
        return tk.Button(center_frame, text=text, font=btn_font, width=30, height=2, command=command)

    if current_user['role'] == 'Адміністратор':
        create_button('Додати користувача', show_add_user_window).pack(pady=5)
        create_button('Керування користувачами', show_users_window).pack(pady=5)

    if current_user['role'] in ['Оператор', 'Адміністратор']:
        create_button('Туристи', show_tourist_window).pack(pady=5)
        create_button('Готелі', show_hotel_window).pack(pady=5)
        create_button('Екскурсії', show_excursion_window).pack(pady=5)
        create_button('Агентства', show_agency_window).pack(pady=5)
        create_button('Вантаж', show_cargo_window).pack(pady=5)
        create_button('Візи', show_visa_window).pack(pady=5)
        create_button('Групи туристів', show_group_window).pack(pady=5)
        create_button('Туриста в групах', show_group_members_window).pack(pady=5)
        create_button('Авіарейси', show_flight_window).pack(pady=5)
        create_button('Фінансові звіти', show_financial_window).pack(pady=5)
        create_button('Аеропортні операції', show_airport_operations_window).pack(pady=5)
        create_button('Митничні процедури', show_customs_procedures_window).pack(pady=5)

    elif current_user['role'] == 'Авторизований':
        create_button('Переглянути туристів', show_tourist_view_window).pack(pady=5)
        create_button('Переглянути готелі', show_hotel_view_window).pack(pady=5)
        create_button('Переглянути екскурсії', show_excursion_view_window).pack(pady=5)
        create_button('Переглянути агентства', show_agency_view_window).pack(pady=5)
        create_button('Переглянути вантаж', show_cargo_view_window).pack(pady=5)
        create_button('Переглянути візи', show_visa_view_window).pack(pady=5)
        create_button('Переглянути групи', show_group_view_window).pack(pady=5)
        create_button('Переглянути авіарейси', show_flight_view_window).pack(pady=5)

    elif current_user['role'] == 'Гість':
        create_button('Переглянути готелі', show_hotel_public_window).pack(pady=5)
        create_button('Переглянути екскурсії', show_excursion_public_window).pack(pady=5)
        create_button('Переглянути агентства', show_agency_public_window).pack(pady=5)

    create_button('Функціональні запити', show_queries_window).pack(pady=5)
    create_button('Заявки', show_requests_window).pack(pady=5)
    create_button('Вийти', logout).pack(pady=5)

    def on_key_press(event):
        if event.keysym == 'F1':
            messagebox.showinfo('Довідка',
                                'Клавішні комбінації:\n'
                                'F1 - Довідка\n'
                                'Escape - Закрити вікно\n'
                                'Enter - Підтвердити дію\n'
                                'Tab - Перехід до наступного поля\n'
                                'Shift+Tab - Перехід до попереднього поля')
        elif event.keysym == 'Escape':
            main_win.destroy()

    main_win.bind('<KeyPress>', on_key_press)
    main_win.focus_set()
    main_win.mainloop()

def logout():
    global current_user
    current_user = None
    
    # Закриваємо всі відкриті вікна Tkinter
    for widget in tk._default_root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
    
    # Закриваємо головне вікно, якщо воно існує
    if tk._default_root:
        tk._default_root.destroy()
    
    # Відкриваємо вікно входу
    show_login_window()

# --- Додавання користувача ---
def show_add_user_window():
    win = tk.Toplevel()
    win.title('Додати користувача')

    tk.Label(win, text='Логін').grid(row=0, column=0, padx=5, pady=5)
    tk.Label(win, text='Пароль').grid(row=1, column=0, padx=5, pady=5)
    tk.Label(win, text='Права').grid(row=2, column=0, padx=5, pady=5)

    width = 25
    entry_login = tk.Entry(win, width=width)
    entry_password = tk.Entry(win, width=width, show='*')
    combo_role = ttk.Combobox(win, values=['Адміністратор', 'Оператор', 'Авторизований', 'Гість'], width=width - 2)
    combo_role.set('Гість')  # Значення за замовчуванням

    entry_login.grid(row=0, column=1, padx=5, pady=5)
    entry_password.grid(row=1, column=1, padx=5, pady=5)
    combo_role.grid(row=2, column=1, padx=5, pady=5)

    def add():
        login_val = entry_login.get()
        password_val = entry_password.get()
        role_val = combo_role.get()

        # Перевірка заповненості полів
        if not login_val or not password_val or not role_val:
            messagebox.showerror('Помилка', 'Будь ласка, заповніть всі поля')
            return

        # Перевірка чи логін вже існує в БД
        if db.user_exists(login_val):
            messagebox.showerror('Помилка', 'Користувач з таким логіном вже існує')
            return

        # Хешування пароля
        hashed_password = hashlib.sha256(password_val.encode('utf-8')).hexdigest()

        if db.add_user(login_val, hashed_password, role_val):
            messagebox.showinfo('Успіх', 'Користувача додано')
            win.destroy()
        else:
            messagebox.showerror('Помилка', 'Не вдалося додати користувача')

    tk.Button(win, text='Додати', command=add).grid(row=3, column=0, columnspan=2, pady=10)


# --- Користувачі (тільки для адміністраторів/операторів) ---
def show_users_window():
    win = tk.Toplevel()
    win.title('Користувачі')
    tree = ttk.Treeview(win, columns=('ID', 'Логін', 'Права'), show='headings')
    for col in ('ID', 'Логін', 'Права'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        for u in db.get_all_users():
            tree.insert('', 'end', values=(u['id'], u['login'], u['role']))

    refresh()

    def edit_user():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть користувача для редагування')
            return
        item = tree.item(sel[0])
        user_id = item['values'][0]
        current_login = item['values'][1]
        current_role = item['values'][2]

        form = tk.Toplevel()
        form.title('Редагувати користувача')

        tk.Label(form, text='Логін').grid(row=0, column=0)
        entry_login = tk.Entry(form, width=30)
        entry_login.insert(0, current_login)
        entry_login.grid(row=0, column=1)

        tk.Label(form, text='Пароль').grid(row=1, column=0)
        entry_password = tk.Entry(form, width=30, show='*')
        entry_password.grid(row=1, column=1)

        tk.Label(form, text='Права').grid(row=2, column=0)
        combo_role = ttk.Combobox(form, values=['Адміністратор', 'Оператор', 'Авторизований', 'Гість'], state='readonly', width=28)
        combo_role.set(current_role)
        combo_role.grid(row=2, column=1)

        def save():
            login_val = entry_login.get().strip()
            password_val = entry_password.get().strip()
            role_val = combo_role.get()

            if not login_val:
                messagebox.showerror('Помилка', 'Логін є обов\'язковим')
                return
            if not role_val:
                messagebox.showerror('Помилка', 'Оберіть роль')
                return

            # If password is empty, do not update it
            if password_val:
                # Хешування пароля перед збереженням
                hashed_password = hashlib.sha256(password_val.encode('utf-8')).hexdigest()
                success = db.update_user(user_id, login_val, hashed_password, role_val)
            else:
                success = db.update_user_without_password(user_id, login_val, role_val)

            if success:
                messagebox.showinfo('Успіх', 'Користувача оновлено')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося оновити користувача')

        tk.Button(form, text='Зберегти', command=save).grid(row=3, column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_user():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть користувача для видалення')
            return
        item = tree.item(sel[0])
        user_id = item['values'][0]
        login_val = item['values'][1]

        result = messagebox.askyesno('Підтвердження', f'Видалити користувача "{login_val}"?')
        if result:
            if db.delete_user(user_id):
                messagebox.showinfo('Успіх', 'Користувача видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити користувача')

    button_frame = tk.Frame(win)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text='Редагувати', command=edit_user).pack(side='left', padx=5)
    tk.Button(button_frame, text='Видалити', command=delete_user).pack(side='left', padx=5)

# --- CRUD-екрани для всіх сутностей ---    
# Приклад для Туристів (аналогічно для інших)
def show_tourist_window():
    win = tk.Toplevel()
    win.title('Туристи')
    tree = ttk.Treeview(win, columns=('ID', 'ПІБ', 'Паспорт', 'Стать', 'Вік', 'Категорія', 'Діти'), show='headings')
    for col in ('ID', 'ПІБ', 'Паспорт', 'Стать', 'Вік', 'Категорія', 'Діти'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children(): tree.delete(i)
        for t in db.get_tourists():
            tree.insert('', 'end', values=(t['id'], t['full_name'], t['passport'], t['gender'], t['age'], t['category'],
                                           t['children_info']))

    refresh()

    def add_tourist():
        form = tk.Toplevel()
        form.title('Додати туриста')

        # Функція для валідації вводу (заборона мінуса)
        def validate_children_input(char):
            return char != '-'

        # Утиліта для плейсхолдерів
        def add_placeholder(entry, placeholder):
            entry.insert(0, placeholder)
            entry.config(fg='grey')

            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg='black')

            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg='grey')

            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)

        # Поля
        tk.Label(form, text='ПІБ').grid(row=0, column=0)
        entry_name = tk.Entry(form, width=30)
        add_placeholder(entry_name, 'Введіть ПІБ')
        entry_name.grid(row=0, column=1)

        tk.Label(form, text='Паспорт').grid(row=1, column=0)
        entry_passport = tk.Entry(form, width=30)
        add_placeholder(entry_passport, 'AA123456')
        entry_passport.grid(row=1, column=1)

        tk.Label(form, text='Стать').grid(row=2, column=0)
        combo_gender = ttk.Combobox(form, values=['чоловіча', 'жіноча'], state='readonly', width=28)
        combo_gender.set('Оберіть стать')
        combo_gender.grid(row=2, column=1)

        tk.Label(form, text='Вік').grid(row=3, column=0)
        entry_age = tk.Entry(form, width=30)
        add_placeholder(entry_age, 'Введіть вік')
        entry_age.grid(row=3, column=1)

        tk.Label(form, text='Категорія').grid(row=4, column=0)
        combo_category = ttk.Combobox(form, values=['відпочинок', 'вантаж'], state='readonly', width=28)
        combo_category.set('Оберіть категорію')
        combo_category.grid(row=4, column=1)

        tk.Label(form, text='Діти').grid(row=5, column=0)
        # Додаємо валідацію для заборони введення мінуса
        vcmd = (form.register(validate_children_input), '%S')
        entry_children = tk.Entry(form, width=30, validate='key', validatecommand=vcmd)
        add_placeholder(entry_children, 'Інформація про дітей')
        entry_children.grid(row=5, column=1)

        def save():
            name = entry_name.get().strip()
            passport = entry_passport.get().strip()
            gender = combo_gender.get()
            age = entry_age.get().strip()
            category = combo_category.get()
            children = entry_children.get().strip()

            # Валідація ПІБ - має бути рівно 3 слова
            if not validate_required(name) or name == 'Введіть ПІБ':
                messagebox.showerror('Помилка', 'ПІБ є обов\'язковим')
                return

            name_words = name.split()
            if len(name_words) != 3:
                messagebox.showerror('Помилка', 'ПІБ повинен містити рівно 3 слова (Прізвище Ім\'я По-батькові)')
                return

            # Валідація паспорту
            if not validate_required(passport) or passport == 'AA123456':
                messagebox.showerror('Помилка', 'Паспорт є обов\'язковим, перевірте чи правильно ви його вписали')
                return

            # Перевірка унікальності паспорту
            existing_tourists = db.get_tourists()
            passport_exists = False
            for tourist in existing_tourists:
                if tourist['passport'] == passport:
                    passport_exists = True
                    break

            if passport_exists:
                messagebox.showerror('Помилка', 'Турист з таким номером паспорта вже існує')
                return

            # Валідація віку
            if not validate_number(age):
                messagebox.showerror('Помилка', 'Вік повинен бути числом')
                return

            age_num = int(age)
            if age_num <= 0:
                messagebox.showerror('Помилка', 'Вік повинен бути більшим за 0')
                return

            # Валідація статі
            if gender not in ['чоловіча', 'жіноча']:
                messagebox.showerror('Помилка', 'Виберіть стать')
                return

            # Валідація категорії
            if category not in ['відпочинок', 'вантаж']:
                messagebox.showerror('Помилка', 'Виберіть категорію (відпочинок/вантаж)')
                return

            # Валідація поля "Діти"
            if children and children != 'Інформація про дітей':
                # Якщо введено число - перевіряємо його
                if children.isdigit():
                    children_num = int(children)
                    if children_num == 0:
                        children = 'немає'
                # Якщо введено текст - залишаємо як є
            else:
                children = 'немає'

            if db.add_tourist(name, passport, gender, age, category, children):
                messagebox.showinfo('Успіх', 'Туриста додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати туриста')

        tk.Button(form, text='Зберегти', command=save).grid(row=6, column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_tourist():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть туриста для редагування')
            return

        item = tree.item(sel[0])
        tourist_id = item['values'][0]
        current_values = item['values'][1:7]  # Пропустити ID

        form = tk.Toplevel()
        form.title('Редагувати туриста')

        # Функція для валідації вводу (заборона мінуса)
        def validate_children_input(char):
            return char != '-'

        # Поле ПІБ
        tk.Label(form, text='ПІБ').grid(row=0, column=0)
        entry_name = tk.Entry(form, width=30)
        entry_name.insert(0, current_values[0])
        entry_name.grid(row=0, column=1)

        # Поле Паспорт
        tk.Label(form, text='Паспорт').grid(row=1, column=0)
        entry_passport = tk.Entry(form, width=30)
        entry_passport.insert(0, current_values[1])
        entry_passport.grid(row=1, column=1)

        # Додаємо мітку для відображення помилки паспорта
        passport_error_label = tk.Label(form, text='', fg='red', font=('Arial', 8))
        passport_error_label.grid(row=2, column=1, sticky='w')

        # Функція для перевірки паспорта в реальному часі
        def check_passport_unique(*args):
            passport = entry_passport.get().strip()
            current_passport = current_values[1]  # Поточний паспорт редагуємого туриста

            # Якщо паспорт не змінився - нічого не перевіряємо
            if passport == current_passport:
                passport_error_label.config(text='')
                return True

            # Перевіряємо чи паспорт не порожній
            if not passport:
                passport_error_label.config(text='')
                return False

            # Використовуємо функцію з queries.py
            is_unique = db.check_passport_unique(passport, tourist_id)

            if not is_unique:
                passport_error_label.config(text='Паспорт вже існує в базі даних')
                return False
            else:
                passport_error_label.config(text='')
                return True

        # Додаємо відстеження змін в полі паспорта
        entry_passport_var = tk.StringVar()
        entry_passport_var.set(current_values[1])
        entry_passport_var.trace('w', check_passport_unique)
        entry_passport.config(textvariable=entry_passport_var)

        # Поле Стать (Combobox)
        tk.Label(form, text='Стать').grid(row=3, column=0)
        combo_gender = ttk.Combobox(form, values=['чоловіча', 'жіноча'], state='readonly', width=28)
        combo_gender.set(current_values[2] if current_values[2] in ['чоловіча', 'жіноча'] else 'Оберіть стать')
        combo_gender.grid(row=3, column=1)

        # Поле Вік
        tk.Label(form, text='Вік').grid(row=4, column=0)
        entry_age = tk.Entry(form, width=30)
        entry_age.insert(0, current_values[3])
        entry_age.grid(row=4, column=1)

        # Поле Категорія (Combobox)
        tk.Label(form, text='Категорія').grid(row=5, column=0)
        combo_category = ttk.Combobox(form, values=['відпочинок', 'вантаж'], state='readonly', width=28)
        combo_category.set(current_values[4] if current_values[4] in ['відпочинок', 'вантаж'] else 'Оберіть категорію')
        combo_category.grid(row=5, column=1)

        # Поле Діти
        tk.Label(form, text='Діти').grid(row=6, column=0)
        # Додаємо валідацію для заборони введення мінуса
        vcmd = (form.register(validate_children_input), '%S')
        entry_children = tk.Entry(form, width=30, validate='key', validatecommand=vcmd)
        children_value = current_values[5] if current_values[5] and current_values[5] != 'немає' else ''
        entry_children.insert(0, children_value)
        entry_children.grid(row=6, column=1)

        def save():
            # Перевіряємо чи паспорт унікальний перед збереженням
            if not check_passport_unique():
                messagebox.showerror('Помилка', 'Паспорт вже існує в базі даних')
                return

            name = entry_name.get().strip()
            passport = entry_passport.get().strip()
            gender = combo_gender.get()
            age = entry_age.get().strip()
            category = combo_category.get()
            children = entry_children.get().strip()

            # Валідація ПІБ - має бути рівно 3 слова
            if not validate_required(name):
                messagebox.showerror('Помилка', 'ПІБ є обов\'язковим')
                return

            name_words = name.split()
            if len(name_words) != 3:
                messagebox.showerror('Помилка', 'ПІБ повинен містити рівно 3 слова (Прізвище Ім\'я По-батькові)')
                return

            # Валідація паспорту
            if not validate_required(passport):
                messagebox.showerror('Помилка', 'Паспорт є обов\'язковим')
                return

            # Валідація віку
            if not validate_number(age):
                messagebox.showerror('Помилка', 'Вік повинен бути числом')
                return

            age_num = int(age)
            if age_num <= 0:
                messagebox.showerror('Помилка', 'Вік повинен бути більшим за 0')
                return

            # Валідація статі
            if gender not in ['чоловіча', 'жіноча']:
                messagebox.showerror('Помилка', 'Виберіть стать')
                return

            # Валідація категорії
            if category not in ['відпочинок', 'вантаж']:
                messagebox.showerror('Помилка', 'Виберіть категорію (відпочинок/вантаж)')
                return

            # Валідація поля "Діти"
            if children:
                # Якщо введено число - перевіряємо його
                if children.isdigit():
                    children_num = int(children)
                    if children_num == 0:
                        children = 'немає'
                # Якщо введено текст - залишаємо як є
            else:
                children = 'немає'

            result = db.update_tourist(tourist_id, name, passport, gender, age, category, children)

            if result is True:
                messagebox.showinfo('Успіх', 'Туриста оновлено')
                form.destroy()
                refresh()
            elif result == 'duplicate_passport':
                messagebox.showerror('Помилка', 'Турист з таким номером паспорта вже існує')
            else:
                messagebox.showerror('Помилка', 'Не вдалося оновити туриста')

        tk.Button(form, text='Зберегти', command=save).grid(row=7, column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_tourist():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть туриста для видалення')
            return
        if messagebox.askyesno('Підтвердження',
                               'Ви впевнені, що хочете видалити цього туриста? Це також видалить всі пов\'язані дані.'):
            tourist_id = tree.item(sel[0])['values'][0]
            if db.delete_tourist(tourist_id):
                messagebox.showinfo('Успіх', 'Туриста видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити туриста')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_tourist).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_tourist).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_tourist).pack(side='left')

# --- Готелі ---
def show_hotel_window():
    win = tk.Toplevel()
    win.title('Готелі')
    tree = ttk.Treeview(win, columns=('ID', 'Назва', 'Адреса', 'К-сть номерів', 'Типи номерів'), show='headings')
    for col in ('ID', 'Назва', 'Адреса', 'К-сть номерів', 'Типи номерів'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    def refresh():
        for i in tree.get_children(): tree.delete(i)
        for h in db.get_hotels():
            tree.insert('', 'end', values=(h['id'], h['name'], h['address'], h['rooms_count'], h['room_types']))
    refresh()

    import re
    from tkinter import messagebox

    def add_hotel():
        form = tk.Toplevel()
        form.title('Додати готель')
        labels = ['Назва', 'Адреса', 'К-сть номерів', 'Типи номерів']
        entries = [tk.Entry(form) for _ in labels]
        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            entries[i].grid(row=i, column=1)

        def save():
            name = entries[0].get().strip()
            address = entries[1].get().strip()
            rooms = entries[2].get().strip()
            room_types = entries[3].get().strip()

            # Перевірка назви
            if not validate_required(name):
                messagebox.showerror('Помилка', 'Назва готелю є обов\'язковою')
                return
            if name.isdigit():
                messagebox.showerror('Помилка', 'Назва готелю не може складатися лише з цифр')
                return

            # Перевірка кількості номерів
            if not validate_required(rooms):
                messagebox.showerror('Помилка', 'Поле "К-сть номерів" є обов\'язковим')
                return
            if not validate_number(rooms):
                messagebox.showerror('Помилка', 'Кількість номерів має бути числом')
                return

            # 🔹 Перевірка типу номерів (не має містити цифр)
            if not validate_required(room_types):
                messagebox.showerror('Помилка', 'Поле "Типи номерів" є обов\'язковим')
                return
            if re.search(r'\d', room_types):
                messagebox.showerror('Помилка', 'Поле "Типи номерів" не може містити цифри')
                return

            if db.add_hotel(name, address, rooms, room_types):
                messagebox.showinfo('Успіх', 'Готель додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати готель')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_hotel():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть готель для редагування')
            return
        item = tree.item(sel[0])
        hotel_id = item['values'][0]

        form = tk.Toplevel()
        form.title('Редагувати готель')
        labels = ['Назва', 'Адреса', 'К-сть номерів', 'Типи номерів']
        entries = [tk.Entry(form) for _ in labels]

        current_values = item['values'][1:5]
        for i, value in enumerate(current_values):
            entries[i].insert(0, str(value))

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            entries[i].grid(row=i, column=1)

        def save():
            name = entries[0].get().strip()
            address = entries[1].get().strip()
            rooms = entries[2].get().strip()
            room_types = entries[3].get().strip()

            # Перевірка назви
            if not validate_required(name):
                messagebox.showerror('Помилка', 'Назва готелю є обов\'язковою')
                return
            if name.isdigit():
                messagebox.showerror('Помилка', 'Назва готелю не може складатися лише з цифр')
                return

            # Перевірка кількості номерів
            if not validate_required(rooms):
                messagebox.showerror('Помилка', 'Поле "К-сть номерів" є обов\'язковим')
                return
            if not validate_number(rooms):
                messagebox.showerror('Помилка', 'Кількість номерів має бути числом')
                return

            # 🔹 Перевірка типу номерів (не має містити цифр)
            if not validate_required(room_types):
                messagebox.showerror('Помилка', 'Поле "Типи номерів" є обов\'язковим')
                return
            if re.search(r'\d', room_types):
                messagebox.showerror('Помилка', 'Поле "Типи номерів" не може містити цифри')
                return

            if db.update_hotel(hotel_id, name, address, rooms, room_types):
                messagebox.showinfo('Успіх', 'Готель оновлено')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося оновити готель')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_hotel():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть готель для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити цей готель?'):
            hotel_id = tree.item(sel[0])['values'][0]
            if db.delete_hotel(hotel_id):
                messagebox.showinfo('Успіх', 'Готель видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити готель')
    
    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_hotel).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_hotel).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_hotel).pack(side='left')

# --- Екскурсії ---
def show_excursion_window():
    win = tk.Toplevel()
    win.title('Екскурсії')
    tree = ttk.Treeview(win, columns=('ID', 'Назва', 'Дата', 'Тривалість', 'Агентство', 'Ціна(грн)'), show='headings')
    for col in ('ID', 'Назва', 'Дата', 'Тривалість', 'Агентство', 'Ціна(грн)'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    # 🔹 Функція перевірки та перетворення HH:MM -> хвилини
    def parse_duration(duration_str):
        match = re.match(r'^([0-9]{1,2}):([0-5][0-9])$', duration_str)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            return hours * 60 + minutes
        return None

    # 🔹 Функція перетворення хвилин -> HH:MM
    def format_duration(minutes):
        h = minutes // 60
        m = minutes % 60
        return f"{h:02}:{m:02}"

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        agencies = {a['id']: a['name'] for a in db.get_excursion_agencies()}
        for e in db.get_excursions():
            agency = agencies.get(e['agency_id'], '')
            duration_str = format_duration(int(e['duration'])) if e['duration'] else ''
            tree.insert('', 'end', values=(
                e['id'], e['name'], e['date'], duration_str, agency, e['price']
            ))

    refresh()

    def add_excursion():
        form = tk.Toplevel()
        form.title('Додати екскурсію')
        labels = ['Назва', 'Дата', 'Тривалість (ГГ:ХХ)', 'Агентство', 'Ціна']
        entry_name = tk.Entry(form)
        entry_date = DateEntry(form, date_pattern='yyyy-mm-dd')
        entry_duration = tk.Entry(form)
        agencies = db.get_excursion_agencies()
        agency_names = [a['name'] for a in agencies]
        combo_agency = ttk.Combobox(form, values=agency_names)
        entry_price = tk.Entry(form)
        widgets = [entry_name, entry_date, entry_duration, combo_agency, entry_price]

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)

        def save():
            duration = parse_duration(entry_duration.get())
            agency_id = agencies[combo_agency.current()]['id'] if combo_agency.current() >= 0 else None

            if not duration:
                messagebox.showerror('Помилка', 'Невірний формат тривалості! Використовуйте ГГ:ХХ')
                return

            if db.add_excursion(
                    entry_name.get(), entry_date.get(), duration, agency_id, entry_price.get()
            ):
                messagebox.showinfo('Успіх', 'Екскурсію додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати екскурсію')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_excursion():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть екскурсію для редагування')
            return
        item = tree.item(sel[0])
        excursion_id = item['values'][0]

        form = tk.Toplevel()
        form.title('Редагувати екскурсію')

        entry_name = tk.Entry(form)
        entry_date = DateEntry(form, date_pattern='yyyy-mm-dd')
        entry_duration = tk.Entry(form)
        agencies = db.get_excursion_agencies()
        agency_names = [a['name'] for a in agencies]
        combo_agency = ttk.Combobox(form, values=agency_names)
        entry_price = tk.Entry(form)

        # Заповнення поточними значеннями
        entry_name.insert(0, item['values'][1])
        entry_date.set_date(item['values'][2])
        entry_duration.insert(0, item['values'][3])  # HH:MM
        combo_agency.set(item['values'][4])
        entry_price.insert(0, item['values'][5])

        labels = ['Назва', 'Дата', 'Тривалість (ГГ:ХХ)', 'Агентство', 'Ціна']
        widgets = [entry_name, entry_date, entry_duration, combo_agency, entry_price]

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)

        def save():
            duration = parse_duration(entry_duration.get())
            price_str = entry_price.get().strip()
            agency_id = agencies[combo_agency.current()]['id'] if combo_agency.current() >= 0 else None

            # 🔹 Валідація тривалості
            if not duration:
                messagebox.showerror('Помилка', 'Невірний формат тривалості! Використовуйте ГГ:ХХ')
                return

            # 🔹 Валідація ціни
            if not price_str:
                messagebox.showerror('Помилка', 'Поле ціни обов’язкове для заповнення!')
                return
            try:
                price = float(price_str)
                if price <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror('Помилка', 'Ціна повинна бути додатнім числом!')
                return

            # 🔹 Збереження
            if db.update_excursion(
                    excursion_id, entry_name.get(), entry_date.get(), duration, agency_id, price
            ):
                messagebox.showinfo('Успіх', 'Екскурсію оновлено')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося оновити екскурсію')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_excursion():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть екскурсію для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити цю екскурсію?'):
            excursion_id = tree.item(sel[0])['values'][0]
            if db.delete_excursion(excursion_id):
                messagebox.showinfo('Успіх', 'Екскурсію видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити екскурсію')
    
    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_excursion).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_excursion).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_excursion).pack(side='left')

# --- Агентства ---
def show_agency_window():
    win = tk.Toplevel()
    win.title('Агентства')

    tree = ttk.Treeview(win, columns=('ID', 'Назва', 'Контакти'), show='headings')
    for col in ('ID', 'Назва', 'Контакти'):
        tree.heading(col, text=col)
        tree.column(col, anchor='center')  # центрування для кращого вигляду

    tree.pack(fill='both', expand=True, padx=10, pady=10)

    def get_all_agencies():
        """Отримати всі агентства для перевірки унікальності"""
        return db.get_excursion_agencies()

    def is_name_unique(name, exclude_id=None):
        """Перевірити унікальність назви агентства"""
        agencies = get_all_agencies()
        for agency in agencies:
            if exclude_id and agency['id'] == exclude_id:
                continue
            if agency['name'].strip().lower() == name.strip().lower():
                return False
        return True

    def is_contact_unique(contact, exclude_id=None):
        """Перевірити унікальність контактної інформації"""
        if not contact.strip():
            return True

        agencies = get_all_agencies()
        for agency in agencies:
            if exclude_id and agency['id'] == exclude_id:
                continue
            if agency['contact_info'].strip().lower() == contact.strip().lower():
                return False
        return True

    def extract_phone_and_email(contacts):
        """Витягти телефон та email з контактної інформації"""
        contacts = contacts.strip()
        phone_pattern = re.compile(r'(\+?\d{10,13})')
        email_pattern = re.compile(r'([\w\.-]+@[\w\.-]+\.\w+)')

        phones = phone_pattern.findall(contacts)
        emails = email_pattern.findall(contacts)

        return phones, emails

    def are_contacts_unique(contacts, exclude_id=None):
        """Перевірити унікальність телефонів та email"""
        if not contacts.strip():
            return True, ""

        phones, emails = extract_phone_and_email(contacts)
        agencies = get_all_agencies()

        for agency in agencies:
            if exclude_id and agency['id'] == exclude_id:
                continue

            agency_phones, agency_emails = extract_phone_and_email(agency['contact_info'])

            # Перевірка телефонів
            for phone in phones:
                if phone in agency_phones:
                    return False, f"Телефон {phone} вже використовується"

            # Перевірка email
            for email in emails:
                if email in agency_emails:
                    return False, f"Email {email} вже використовується"

        return True, ""

    def validate_contacts(value):
        """Перевірка, що введено телефон або email."""
        value = value.strip()
        if not value:
            return False

        # Простий патерн для телефону (+380XXXXXXXXX)
        phone_pattern = re.compile(r'(\+?\d{10,13})')
        # Простий патерн для email
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

        # Перевірка
        if phone_pattern.search(value) or email_pattern.search(value):
            return True
        return False

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        for a in db.get_excursion_agencies():
            tree.insert('', 'end', values=(a['id'], a['name'], a['contact_info']))

        # Оновлюємо розміри вікна після завантаження даних
        win.update_idletasks()
        win.geometry(f"{tree.winfo_reqwidth() + 40}x{tree.winfo_reqheight() + 40}")

    refresh()

    def add_agency():
        form = tk.Toplevel()
        form.title('Додати агентство')
        labels = ['Назва', 'Контакти']
        entries = [tk.Entry(form) for _ in labels]

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            entries[i].grid(row=i, column=1)

        # --- Додаємо placeholder для контактів ---
        placeholder = "Телефон: ..., Email: ..."
        contacts_entry = entries[1]
        contacts_entry.insert(0, placeholder)
        contacts_entry.config(fg='grey')

        def on_focus_in(event):
            if contacts_entry.get() == placeholder:
                contacts_entry.delete(0, 'end')
                contacts_entry.config(fg='black')

        def on_focus_out(event):
            if not contacts_entry.get():
                contacts_entry.insert(0, placeholder)
                contacts_entry.config(fg='grey')

        contacts_entry.bind("<FocusIn>", on_focus_in)
        contacts_entry.bind("<FocusOut>", on_focus_out)

        # ------------------------------------------

        def save():
            name = entries[0].get().strip()
            contacts = entries[1].get().strip()
            if contacts == placeholder:
                contacts = ""  # Якщо користувач нічого не ввів

            if not name:
                messagebox.showerror('Помилка', 'Заповніть назву агентства')
                return
            if not validate_contacts(contacts):
                messagebox.showerror('Помилка', 'Вкажіть хоча б телефон або email')
                return

            if not is_name_unique(name):
                messagebox.showerror('Помилка', 'Агентство з такою назвою вже існує')
                return

            contacts_unique, error_msg = are_contacts_unique(contacts)
            if not contacts_unique:
                messagebox.showerror('Помилка', error_msg)
                return

            if db.add_excursion_agency(name, contacts):
                messagebox.showinfo('Успіх', 'Агентство додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати агентство')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_agency():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть агентство для редагування')
            return
        item = tree.item(sel[0])
        agency_id = item['values'][0]

        form = tk.Toplevel()
        form.title('Редагувати агентство')
        labels = ['Назва', 'Контакти']
        entries = [tk.Entry(form) for _ in labels]

        # Заповнення поточними значеннями
        entries[0].insert(0, item['values'][1])
        entries[1].insert(0, item['values'][2])

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            entries[i].grid(row=i, column=1)

        def save():
            name = entries[0].get().strip()
            contacts = entries[1].get().strip()

            if not name:
                messagebox.showerror('Помилка', 'Заповніть назву агентства')
                return
            if not validate_contacts(contacts):
                messagebox.showerror('Помилка', 'Вкажіть хоча б телефон або email')
                return

            # Перевірка унікальності назви (виключаючи поточне агентство)
            if not is_name_unique(name, agency_id):
                messagebox.showerror('Помилка', 'Агентство з такою назвою вже існує')
                return

            # Перевірка унікальності контактів (виключаючи поточне агентство)
            contacts_unique, error_msg = are_contacts_unique(contacts, agency_id)
            if not contacts_unique:
                messagebox.showerror('Помилка', error_msg)
                return

            if db.update_excursion_agency(agency_id, name, contacts):
                messagebox.showinfo('Успіх', 'Агентство оновлено')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося оновити агентство')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_agency():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть агентство для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити це агентство?'):
            agency_id = tree.item(sel[0])['values'][0]
            if db.delete_excursion_agency(agency_id):
                messagebox.showinfo('Успіх', 'Агентство видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити агентство')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_agency).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_agency).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_agency).pack(side='left')

# --- Вантаж ---
def show_cargo_window():
    win = tk.Toplevel()
    win.title('Вантаж')
    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'К-сть валіз', 'Вага(кг)', 'Вартість упаковки(грн)', 'Страховка(грн)', 'Підсумок(грн)'), show='headings')
    for col in ('ID', 'Турист', 'К-сть валіз', 'Вага(кг)', 'Вартість упаковки(грн)', 'Страховка(грн)', 'Підсумок(грн)'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    def refresh():
        for i in tree.get_children(): tree.delete(i)
        tourists = {t['id']: t['full_name'] for t in db.get_tourists()}
        for c in db.get_cargos():
            tourist = tourists.get(c['tourist_id'], '')
            tree.insert('', 'end', values=(c['id'], tourist, c['places_count'], c['weight'], c['packing_cost'], c['insurance'], c['total']))
    refresh()

    def add_cargo():
        form = tk.Toplevel()
        form.title('Додати вантаж')

        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])

        labels = ['К-сть валіз', 'Вага', 'Вартість упаковки', 'Страховка', 'Підсумок']
        entries = [tk.Entry(form) for _ in labels]

        tk.Label(form, text='Турист').grid(row=0, column=0)
        combo_tourist.grid(row=0, column=1)

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i + 1, column=0)
            entries[i].grid(row=i + 1, column=1)

        # Робимо підсумок тільки для читання
        entries[4].config(state='readonly')

        # Функція для автоматичного обчислення підсумку
        def calculate_total():
            try:
                count = int(entries[0].get())
                packing = float(entries[2].get())
                insurance = float(entries[3].get())
                total = count * (packing + insurance)
                entries[4].config(state='normal')
                entries[4].delete(0, tk.END)
                entries[4].insert(0, f"{total:.2f}")
                entries[4].config(state='readonly')
            except ValueError:
                entries[4].config(state='normal')
                entries[4].delete(0, tk.END)
                entries[4].insert(0, "0.00")
                entries[4].config(state='readonly')

        # Прив'язка обчислення підсумку до змін полів
        for i in [0, 2, 3]:  # К-сть валіз, Вартість упаковки, Страховка
            entries[i].bind('<KeyRelease>', lambda e: calculate_total())

        def save():
            tourist_id = tourists[combo_tourist.current()]['id'] if combo_tourist.current() >= 0 else None
            if all(validate_number(e.get()) for e in entries[:4]) and tourist_id:  # Перевіряємо тільки числові поля
                if db.add_cargo(tourist_id, *(e.get() for e in entries)):
                    messagebox.showinfo('Успіх', 'Вантаж додано')
                    form.destroy();
                    refresh()
                else:
                    messagebox.showerror('Помилка', 'Не вдалося додати вантаж')
            else:
                messagebox.showerror('Помилка', 'Перевірте правильність введених даних')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels) + 1, column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_cargo():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть вантаж для редагування')
            return
        item = tree.item(sel[0])
        cargo_id = item['values'][0]

        form = tk.Toplevel()
        form.title('Редагувати вантаж')

        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])

        labels = ['К-сть валіз', 'Вага', 'Вартість упаковки', 'Страховка', 'Підсумок']
        entries = [tk.Entry(form) for _ in labels]

        # Заповнення поточними значеннями
        combo_tourist.set(item['values'][1])  # Турист
        for i, value in enumerate(item['values'][2:7]):  # Пропустити ID та туриста
            entries[i].insert(0, str(value))

        tk.Label(form, text='Турист').grid(row=0, column=0)
        combo_tourist.grid(row=0, column=1)

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i + 1, column=0)
            entries[i].grid(row=i + 1, column=1)

        # Робимо підсумок тільки для читання
        entries[4].config(state='readonly')

        # Функція для обчислення підсумку
        def calculate_total():
            try:
                count = int(entries[0].get())
                packing = float(entries[2].get())
                insurance = float(entries[3].get())
                total = count * (packing + insurance)
                entries[4].config(state='normal')
                entries[4].delete(0, tk.END)
                entries[4].insert(0, f"{total:.2f}")
                entries[4].config(state='readonly')
            except ValueError:
                entries[4].config(state='normal')
                entries[4].delete(0, tk.END)
                entries[4].insert(0, "0.00")
                entries[4].config(state='readonly')

        # Прив'язка обчислення підсумку до змін полів
        for i in [0, 2, 3]:
            entries[i].bind('<KeyRelease>', lambda e: calculate_total())

        calculate_total()  # щоб підсумок відобразився одразу при відкритті

        def save():
            tourist_id = tourists[combo_tourist.current()]['id'] if combo_tourist.current() >= 0 else None
            if all(validate_number(e.get()) for e in entries[:4]) and tourist_id:
                if db.update_cargo(cargo_id, tourist_id, *(e.get() for e in entries)):
                    messagebox.showinfo('Успіх', 'Вантаж оновлено')
                    form.destroy();
                    refresh()
                else:
                    messagebox.showerror('Помилка', 'Не вдалося оновити вантаж')
            else:
                messagebox.showerror('Помилка', 'Перевірте правильність введених даних')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels) + 1, column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_cargo():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть вантаж для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити цей вантаж?'):
            cargo_id = tree.item(sel[0])['values'][0]
            if db.delete_cargo(cargo_id):
                messagebox.showinfo('Успіх', 'Вантаж видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити вантаж')
    
    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_cargo).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_cargo).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_cargo).pack(side='left')

# --- Візи ---
def show_visa_window():
    win = tk.Toplevel()
    win.title('Візи')

    # Таблиця віз
    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'Номер', 'Дата видачі', 'Країна', 'Термін дії'), show='headings')
    for col in ('ID', 'Турист', 'Номер', 'Дата видачі', 'Країна', 'Термін дії'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    # Функція оновлення даних
    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        tourists_dict = {t['id']: t['full_name'] for t in db.get_tourists()}
        for v in db.get_visas():
            tourist = tourists_dict.get(v['tourist_id'], '')
            tree.insert('', 'end',
                        values=(v['id'], tourist, v['visa_number'], v['issue_date'], v['country'], v['expiry_date']))

    refresh()

    # Форма додавання візи
    def add_visa():
        form = tk.Toplevel()
        form.title('Додати візу')

        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])
        entry_number = tk.Entry(form)
        entry_issue = DateEntry(form, date_pattern='yyyy-mm-dd')
        entry_country = tk.Entry(form)
        entry_expiry = DateEntry(form, date_pattern='yyyy-mm-dd')

        # Розташування полів
        tk.Label(form, text='Турист').grid(row=0, column=0)
        combo_tourist.grid(row=0, column=1)
        tk.Label(form, text='Номер').grid(row=1, column=0)
        entry_number.grid(row=1, column=1)
        tk.Label(form, text='Дата видачі').grid(row=2, column=0)
        entry_issue.grid(row=2, column=1)
        tk.Label(form, text='Країна').grid(row=3, column=0)
        entry_country.grid(row=3, column=1)
        tk.Label(form, text='Термін дії').grid(row=4, column=0)
        entry_expiry.grid(row=4, column=1)

        # Функція збереження
        def save():
            tourist_index = combo_tourist.current()
            tourist_id = tourists[tourist_index]['id'] if tourist_index >= 0 else None

            issue_date = entry_issue.get()
            expiry_date = entry_expiry.get()
            visa_number = entry_number.get().strip()
            country = entry_country.get().strip()

            today = datetime.today().date()

            # Перевірки обов'язкових полів
            if tourist_id is None:
                messagebox.showwarning('Помилка', 'Оберіть туриста')
                return
            if not visa_number:
                messagebox.showwarning('Помилка', 'Вкажіть номер візи')
                return
            if not country:
                messagebox.showwarning('Помилка', 'Вкажіть країну')
                return

            try:
                issue_dt = datetime.strptime(issue_date, '%Y-%m-%d').date()
                expiry_dt = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror('Помилка', 'Невірний формат дати')
                return

            if issue_dt > today:
                messagebox.showerror('Помилка', 'Дата видачі не може бути в майбутньому')
                return
            if expiry_dt < today:
                messagebox.showerror('Помилка', 'Термін дії візи не може бути в минулому')
                return
            if expiry_dt < issue_dt:
                messagebox.showerror('Помилка', 'Термін дії не може бути раніше дати видачі')
                return

            # --- НОВІ ПЕРЕВІРКИ ---
            visas = db.get_visas()

            # Перевірка: один турист не може мати декілька віз
            for v in visas:
                if v['tourist_id'] == tourist_id:
                    messagebox.showerror('Помилка', 'Цей турист вже має візу')
                    return

            # Перевірка: номер візи унікальний
            for v in visas:
                if v['visa_number'].lower() == visa_number.lower():
                    messagebox.showerror('Помилка', 'Цей номер візи вже існує')
                    return

            # Додавання візи
            if db.add_visa(tourist_id, visa_number, issue_date, country, expiry_date):
                messagebox.showinfo('Успіх', 'Візу додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати візу')

        tk.Button(form, text='Зберегти', command=save).grid(row=5, column=0, columnspan=2)

    tk.Button(win, text='Додати', command=add_visa).pack()

# --- Групи туристів ---
def show_group_window():
    win = tk.Toplevel()
    win.title('Групи туристів')
    tree = ttk.Treeview(win, columns=('ID', 'Ідентифікатор', 'Дата прильоту', 'Дата відльоту'), show='headings')
    for col in ('ID', 'Ідентифікатор', 'Дата прильоту', 'Дата відльоту'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    def refresh():
        for i in tree.get_children(): tree.delete(i)
        for g in db.get_tourist_groups():
            tree.insert('', 'end', values=(g['id'], g['group_identifier'], g['arrival_date'], g['departure_date']))
    refresh()
    def add_group():
        form = tk.Toplevel()
        form.title('Додати групу')
        entry_id = tk.Entry(form)
        entry_arrival = DateEntry(form, date_pattern='yyyy-mm-dd')
        entry_departure = DateEntry(form, date_pattern='yyyy-mm-dd')
        tk.Label(form, text='Ідентифікатор').grid(row=0, column=0)
        entry_id.grid(row=0, column=1)
        tk.Label(form, text='Дата прильоту').grid(row=1, column=0)
        entry_arrival.grid(row=1, column=1)
        tk.Label(form, text='Дата відльоту').grid(row=2, column=0)
        entry_departure.grid(row=2, column=1)
        def save():
            if db.add_tourist_group(entry_id.get(), entry_arrival.get(), entry_departure.get()):
                messagebox.showinfo('Успіх', 'Групу додано')
                form.destroy(); refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати групу')
        tk.Button(form, text='Зберегти', command=save).grid(row=3, column=0, columnspan=2)
    tk.Button(win, text='Додати', command=add_group).pack()

# --- Show group members and add tourists to group ---
def show_group_members_window():
    win = tk.Toplevel()
    win.title('Учасники груп')

    # Таблиця учасників груп (без телефону)
    tree = ttk.Treeview(win, columns=('ID', 'Група', 'Турист', 'Паспорт'), show='headings')
    for col in ('ID', 'Група', 'Турист', 'Паспорт'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    # Функція оновлення даних
    def refresh():
        for i in tree.get_children():
            tree.delete(i)

        groups_dict = {g['id']: g['group_identifier'] for g in db.get_tourist_groups()}
        tourists_dict = {t['id']: t for t in db.get_tourists()}

        # Отримати всі зв'язки груп і туристів
        all_groups = db.get_tourist_groups()
        for group in all_groups:
            tourists_in_group = db.get_tourists_in_group(group['id'])
            for tourist in tourists_in_group:
                tree.insert('', 'end', values=(
                    f"{group['id']}-{tourist['id']}",  # Унікальний ID для зв'язку
                    groups_dict.get(group['id'], ''),
                    tourist['full_name'],
                    tourist['passport']
                ))

    refresh()

    # Форма додавання туриста до групи
    def add_member():
        form = tk.Toplevel()
        form.title('Додати туриста до групи')

        groups = db.get_tourist_groups()
        tourists = db.get_tourists()

        combo_group = ttk.Combobox(form, values=[g['group_identifier'] for g in groups])
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])

        # Розташування полів
        tk.Label(form, text='Група').grid(row=0, column=0)
        combo_group.grid(row=0, column=1)
        tk.Label(form, text='Турист').grid(row=1, column=0)
        combo_tourist.grid(row=1, column=1)

        # Функція збереження
        def save():
            group_index = combo_group.current()
            tourist_index = combo_tourist.current()

            group_id = groups[group_index]['id'] if group_index >= 0 else None
            tourist_id = tourists[tourist_index]['id'] if tourist_index >= 0 else None

            # Перевірки
            if group_id is None:
                messagebox.showwarning('Помилка', 'Оберіть групу')
                return
            if tourist_id is None:
                messagebox.showwarning('Помилка', 'Оберіть туриста')
                return

            # Перевірка чи турист вже є у будь-якій групі
            all_groups = db.get_tourist_groups()
            for g in all_groups:
                tourists_in_group = db.get_tourists_in_group(g['id'])
                if any(t['id'] == tourist_id for t in tourists_in_group):
                    messagebox.showwarning('Помилка', f'Турист вже є в групі "{g["group_identifier"]}"')
                    return

            # Додавання туриста до групи
            if db.add_tourist_to_group(group_id, tourist_id):
                messagebox.showinfo('Успіх', 'Туриста додано до групи')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати туриста до групи')

        tk.Button(form, text='Зберегти', command=save).grid(row=2, column=0, columnspan=2)

    # Функція видалення туриста з групи
    def remove_member():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning('Помилка', 'Оберіть запис для видалення')
            return

        # Отримати дані з вибраного рядка
        item_values = tree.item(selected_item[0])['values']
        group_name = item_values[1]
        tourist_name = item_values[2]

        # Знайти group_id та tourist_id
        groups = db.get_tourist_groups()
        tourists = db.get_tourists()

        group_id = None
        tourist_id = None

        for group in groups:
            if group['group_identifier'] == group_name:
                group_id = group['id']
                break

        for tourist in tourists:
            if tourist['full_name'] == tourist_name:
                tourist_id = tourist['id']
                break

        if group_id is None or tourist_id is None:
            messagebox.showerror('Помилка', 'Не вдалося знайти групу або туриста')
            return

        # Підтвердження видалення
        result = messagebox.askyesno('Підтвердження',
                                     f'Видалити туриста "{tourist_name}" з групи "{group_name}"?')

        if result:
            if db.remove_tourist_from_group(group_id, tourist_id):
                messagebox.showinfo('Успіх', 'Туриста видалено з групи')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити туриста з групи')

    # Кнопки
    button_frame = tk.Frame(win)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text='Додати', command=add_member).pack(side='left', padx=5)
    tk.Button(button_frame, text='Видалити', command=remove_member).pack(side='left', padx=5)

# --- Авіарейси ---
def show_flight_window():
    win = tk.Toplevel()
    win.title('Авіарейси')
    tree = ttk.Treeview(win, columns=('ID', 'Номер рейсу', 'Дата', 'К-сть місць', 'Вільні місця', 'Вага вантажу', 'Клас літака'), show='headings')
    for col in ('ID', 'Номер рейсу', 'Дата', 'К-сть місць', 'Вільні місця', 'Вага вантажу', 'Клас літака'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    def refresh():
        for i in tree.get_children(): tree.delete(i)
        for f in db.get_flights():
            tree.insert('', 'end', values=(f['id'], f['flight_number'], f['date'], f['seats_count'], f['free_seats'], f['cargo_weight'], f['plane_class']))
    refresh()

    def add_flight():
        form = tk.Toplevel()
        form.title('Додати авіарейс')

        labels = ['Номер рейсу', 'Дата', 'К-сть місць', 'Вільні місця', 'Вага вантажу', 'Клас літака']
        entry_number = tk.Entry(form)
        entry_date = DateEntry(form, date_pattern='yyyy-mm-dd')
        entry_seats = tk.Entry(form)
        entry_free = tk.Entry(form)
        entry_weight = tk.Entry(form)
        entry_class = tk.Entry(form)

        widgets = [entry_number, entry_date, entry_seats, entry_free, entry_weight, entry_class]
        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0, padx=5, pady=5, sticky='w')
            widgets[i].grid(row=i, column=1, padx=5, pady=5)

        def save():
            # перевірка заповненості
            values = [w.get() for w in widgets]
            if any(v.strip() == '' for v in values):
                messagebox.showerror('Помилка', 'Усі поля мають бути заповнені!')
                return

            # перевірка числових значень
            try:
                seats = int(entry_seats.get())
                free = int(entry_free.get())
                weight = float(entry_weight.get())
            except ValueError:
                messagebox.showerror('Помилка',
                                     'Поля "К-сть місць", "Вільні місця" та "Вага вантажу" мають містити тільки числа!')
                return

            # логічна перевірка кількості
            if free > seats:
                messagebox.showerror('Помилка',
                                     'Кількість вільних місць не може перевищувати загальну кількість місць!')
                return

            # збереження у БД
            if db.add_flight(entry_number.get(), entry_date.get(), seats, free, weight, entry_class.get()):
                messagebox.showinfo('Успіх', 'Авіарейс додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати авіарейс')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2, pady=10)

    tk.Button(win, text='Додати', command=add_flight).pack()

# --- Фінансові звіти ---
def show_financial_window():
    win = tk.Toplevel()
    win.title('Фінансові звіти')
    tree = ttk.Treeview(win, columns=('ID', 'Група', 'Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж'), show='headings')
    for col in ('ID', 'Група', 'Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    def refresh():
        for i in tree.get_children(): tree.delete(i)
        groups = {g['id']: g['group_identifier'] for g in db.get_tourist_groups()}
        for f in db.get_financial_reports():
            group = groups.get(f['group_id'], '')
            tree.insert('', 'end', values=(f['id'], group, f['income'], f['expense_hotel'], f['expense_transport'], f['expense_excursion'], f['expense_airport'], f['expense_cargo']))
    refresh()
    def add_financial():
        form = tk.Toplevel()
        form.title('Додати фінансовий звіт')
        groups = db.get_tourist_groups()
        combo_group = ttk.Combobox(form, values=[g['group_identifier'] for g in groups])
        labels = ['Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж']
        entries = [tk.Entry(form) for _ in labels]
        tk.Label(form, text='Група').grid(row=0, column=0)
        combo_group.grid(row=0, column=1)
        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i+1, column=0)
            entries[i].grid(row=i+1, column=1)

        def save():
            # Перевірка чи вибрано групу
            if combo_group.current() < 0:
                messagebox.showerror('Помилка', 'Оберіть групу')
                return

            values = []
            labels_ua = ['Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж']

            # Перевірка всіх полів
            for i, e in enumerate(entries):
                val = e.get().strip()
                if not val:
                    messagebox.showerror('Помилка', f'Поле "{labels_ua[i]}" не може бути порожнім')
                    return
                try:
                    num = float(val)
                    if num < 0:
                        messagebox.showerror('Помилка', f'Поле "{labels_ua[i]}" не може бути відʼємним')
                        return
                    values.append(num)
                except ValueError:
                    messagebox.showerror('Помилка', f'Поле "{labels_ua[i]}" повинно бути числом')
                    return

            group_id = groups[combo_group.current()]['id']

            if db.add_financial_report(group_id, *values):
                messagebox.showinfo('Успіх', 'Звіт додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати звіт')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels)+1, column=0, columnspan=2)
    tk.Button(win, text='Додати', command=add_financial).pack()

# --- Вікно функціональних запитів з обмеженнями ---
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

        # Перехоплюємо подію закриття
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
            # Словник для перетворення технічних назв полів в зрозумілі користувацькі
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
                # Отримуємо оригінальні назви колонок з першого запису
                original_columns = list(res[0].keys())

                # Виключаємо поле 'id' з відображення
                columns_to_display = [col for col in original_columns if col != 'id']

                # Створюємо список зрозумілих назв колонок (без ID)
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]

                # Формуємо дані для відображення (без поля ID)
                data = [tuple(item[col] for col in columns_to_display) for item in res]

            else:
                display_columns = []
                data = []

            # Відображаємо таблицю з зрозумілими назвами колонок (без ID)
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
            # Словник для перетворення технічних назв полів в зрозумілі користувацькі
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
                # Отримуємо оригінальні назви колонок
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []

                # Створюємо список зрозумілих назв колонок
                display_columns = [FIELD_NAMES.get(col, col) for col in original_columns]

                # Формуємо дані для відображення
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
            # Словник для перетворення технічних назв полів в зрозумілі користувацькі
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
                # Отримуємо оригінальні назви колонок
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []

                # Створюємо список зрозумілих назв колонок
                display_columns = [FIELD_NAMES.get(col, col) for col in original_columns]

                # Формуємо дані для відображення
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
            # Словник для перетворення технічних назв полів в зрозумілі користувацькі
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
                # Отримуємо оригінальні назви колонок
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []

                # Створюємо список зрозумілих назв колонок
                display_columns = [FIELD_NAMES.get(col, col) for col in original_columns]

                # Формуємо дані для відображення
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
                # Створюємо таблицю з двома колонками: Характеристика та Значення
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
            # Словник для перетворення технічних назв полів в зрозумілі користувацькі
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
                # Отримуємо оригінальні назви колонок
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []

                # Виключаємо поле 'id' з відображення
                columns_to_display = [col for col in original_columns if col != 'id']

                # Створюємо список зрозумілих назв колонок
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]

                # Формуємо дані для відображення
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
            # Словник для перетворення технічних назв полів в зрозумілі користувацькі
            FIELD_NAMES = {
                'name': 'Назва готелю',
                'tourists_count': 'Кількість туристів',
                'rooms_occupied': 'Зайнято кімнат',
            }

            res = db.get_hotel_occupancy(date_from.get(), date_to.get())
            if res:
                # Отримуємо оригінальні назви колонок
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []

                # Виключаємо поле 'id' з відображення
                columns_to_display = [col for col in original_columns if col != 'id']

                # Створюємо список зрозумілих назв колонок
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]

                # Формуємо дані для відображення
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
            # Словник для перетворення технічних назв полів в зрозумілі користувацькі
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
                # Отримуємо оригінальні назви колонок
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []

                # Виключаємо поле 'id' з відображення
                columns_to_display = [col for col in original_columns if col != 'id']

                # Створюємо список зрозумілих назв колонок
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]

                # Формуємо дані для відображення
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
            # Словник для перетворення технічних назв полів в зрозумілі користувацькі
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
                # Отримуємо оригінальні назви колонок
                original_columns = list(res[0].keys()) if isinstance(res, list) and len(res) > 0 else []

                # Виключаємо поле 'id' з відображення
                columns_to_display = [col for col in original_columns if col != 'id']

                # Створюємо список зрозумілих назв колонок
                display_columns = [FIELD_NAMES.get(col, col) for col in columns_to_display]

                # Формуємо дані для відображення
                data = [tuple(item[col] for col in columns_to_display) for item in res] if columns_to_display else []



            else:
                display_columns = []
                data = []


            display_table('Туристи за період', display_columns, data, query_name='Туристи за період', raw_result=res)

        tk.Button(form, text='Показати', command=run).grid(row=3, column=0, columnspan=2)

    tk.Button(win, text='Список туристів за період', command=show_tourists_by_period).pack(fill='x')

# --- Вікно заявок ---
def show_requests_window():
    win = tk.Toplevel()
    win.title('Заявки')
    tree = ttk.Treeview(win, columns=('ID', 'Користувач', 'Статус', 'Дата'), show='headings')
    for col in ('ID', 'Користувач', 'Статус', 'Дата'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for r in db.get_requests():
        tree.insert('', 'end', values=(r['id'], r['login'], r['status'], r['request_date']))
    if current_user['role'] == 'Гість':
        def send_request():
            if db.add_request(current_user['id']):
                messagebox.showinfo('Успіх', 'Заявку подано')
                win.destroy()
            else:
                messagebox.showerror('Помилка', 'Не вдалося подати заявку')
        tk.Button(win, text='Подати заявку', command=send_request).pack()
    if current_user['role'] == 'Адміністратор':
        def approve():
            sel = tree.selection()
            if sel:
                rid = tree.item(sel[0])['values'][0]
                db.update_request_status(rid, 'Схвалено')
                request = db.get_request_by_id(rid)
                if request:
                    user_id = request['user_id']
                    db.update_user_role(user_id, 'Авторизований')
                win.destroy()
                show_requests_window()
        def reject():
            sel = tree.selection()
            if sel:
                rid = tree.item(sel[0])['values'][0]
                db.update_request_status(rid, 'Відхилено')
                win.destroy(); show_requests_window()
        tk.Button(win, text='Схвалити', command=approve).pack(side='left')
        tk.Button(win, text='Відхилити', command=reject).pack(side='left')

# --- Функції перегляду (без можливості редагування) для гостей та авторизованих ---
def show_tourist_view_window():
    win = tk.Toplevel()
    win.title('Перегляд туристів')
    tree = ttk.Treeview(win, columns=('ID', 'ПІБ', 'Паспорт', 'Стать', 'Вік', 'Категорія', 'Діти'), show='headings')
    for col in ('ID', 'ПІБ', 'Паспорт', 'Стать', 'Вік', 'Категорія', 'Діти'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for t in db.get_tourists():
        tree.insert('', 'end', values=(t['id'], t['full_name'], t['passport'], t['gender'], t['age'], t['category'], t['children_info']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_hotel_view_window():
    win = tk.Toplevel()
    win.title('Перегляд готелів')
    tree = ttk.Treeview(win, columns=('ID', 'Назва', 'Адреса', 'К-сть номерів', 'Типи номерів'), show='headings')
    for col in ('ID', 'Назва', 'Адреса', 'К-сть номерів', 'Типи номерів'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for h in db.get_hotels():
        tree.insert('', 'end', values=(h['id'], h['name'], h['address'], h['rooms_count'], h['room_types']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_excursion_view_window():
    win = tk.Toplevel()
    win.title('Перегляд екскурсій')
    tree = ttk.Treeview(win, columns=('ID', 'Назва', 'Дата', 'Тривалість', 'Агентство', 'Ціна'), show='headings')
    for col in ('ID', 'Назва', 'Дата', 'Тривалість', 'Агентство', 'Ціна'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    agencies = {a['id']: a['name'] for a in db.get_excursion_agencies()}
    for e in db.get_excursions():
        agency = agencies.get(e['agency_id'], '')
        tree.insert('', 'end', values=(e['id'], e['name'], e['date'], e['duration'], agency, e['price']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_agency_view_window():
    win = tk.Toplevel()
    win.title('Перегляд агентств')
    tree = ttk.Treeview(win, columns=('ID', 'Назва', 'Контакти'), show='headings')
    for col in ('ID', 'Назва', 'Контакти'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for a in db.get_excursion_agencies():
        tree.insert('', 'end', values=(a['id'], a['name'], a['contact_info']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_cargo_view_window():
    win = tk.Toplevel()
    win.title('Перегляд вантажу')
    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'К-сть місць', 'Вага', 'Вартість упаковки', 'Страховка', 'Підсумок'), show='headings')
    for col in ('ID', 'Турист', 'К-сть місць', 'Вага', 'Вартість упаковки', 'Страховка', 'Підсумок'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    tourists = {t['id']: t['full_name'] for t in db.get_tourists()}
    for c in db.get_cargos():
        tourist = tourists.get(c['tourist_id'], '')
        tree.insert('', 'end', values=(c['id'], tourist, c['places_count'], c['weight'], c['packing_cost'], c['insurance'], c['total']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_visa_view_window():
    win = tk.Toplevel()
    win.title('Перегляд віз')
    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'Номер', 'Дата видачі', 'Країна', 'Термін дії'), show='headings')
    for col in ('ID', 'Турист', 'Номер', 'Дата видачі', 'Країна', 'Термін дії'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    tourists = {t['id']: t['full_name'] for t in db.get_tourists()}
    for v in db.get_visas():
        tourist = tourists.get(v['tourist_id'], '')
        tree.insert('', 'end', values=(v['id'], tourist, v['visa_number'], v['issue_date'], v['country'], v['expiry_date']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_group_view_window():
    win = tk.Toplevel()
    win.title('Перегляд груп туристів')
    tree = ttk.Treeview(win, columns=('ID', 'Ідентифікатор', 'Дата прильоту', 'Дата відльоту'), show='headings')
    for col in ('ID', 'Ідентифікатор', 'Дата прильоту', 'Дата відльоту'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for g in db.get_tourist_groups():
        tree.insert('', 'end', values=(g['id'], g['group_identifier'], g['arrival_date'], g['departure_date']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_flight_view_window():
    win = tk.Toplevel()
    win.title('Перегляд авіарейсів')
    tree = ttk.Treeview(win, columns=('ID', 'Номер рейсу', 'Дата', 'К-сть місць', 'Вільні місця', 'Вага вантажу', 'Клас літака'), show='headings')
    for col in ('ID', 'Номер рейсу', 'Дата', 'К-сть місць', 'Вільні місця', 'Вага вантажу', 'Клас літака'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for f in db.get_flights():
        tree.insert('', 'end', values=(f['id'], f['flight_number'], f['date'], f['seats_count'], f['free_seats'], f['cargo_weight'], f['plane_class']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_financial_view_window():
    win = tk.Toplevel()
    win.title('Перегляд фінансових звітів')
    tree = ttk.Treeview(win, columns=('ID', 'Група', 'Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж'), show='headings')
    for col in ('ID', 'Група', 'Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    groups = {g['id']: g['group_identifier'] for g in db.get_tourist_groups()}
    for f in db.get_financial_reports():
        group = groups.get(f['group_id'], '')
        tree.insert('', 'end', values=(f['id'], group, f['income'], f['expense_hotel'], f['expense_transport'], f['expense_excursion'], f['expense_airport'], f['expense_cargo']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_airport_operations_window():
    win = tk.Toplevel()
    win.title('Аеропортні операції')
    tree = ttk.Treeview(win, columns=('ID', 'Рейс', 'Тип операції', 'Опис', 'Вартість(грн)', 'Дата'), show='headings')
    for col in ('ID', 'Рейс', 'Тип операції', 'Опис', 'Вартість(грн)', 'Дата'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    def refresh():
        for i in tree.get_children(): tree.delete(i)
        flights = {f['id']: f['flight_number'] for f in db.get_flights()}
        for op in db.get_airport_operations():
            flight = flights.get(op['flight_id'], '')
            tree.insert('', 'end', values=(op['id'], flight, op['operation_type'], op['description'], op['cost'], op['operation_date']))
    refresh()
    def add_airport_operation():
        form = tk.Toplevel()
        form.title('Додати аеропортну операцію')
        flights = db.get_flights()
        combo_flight = ttk.Combobox(form, values=[f['flight_number'] for f in flights])
        combo_type = ttk.Combobox(form, values=['Прийом', 'Розвантаження', 'Зліт', 'Посадка', 'Диспетчерські послуги'])
        entry_description = tk.Entry(form)
        entry_cost = tk.Entry(form)
        
        labels = ['Рейс', 'Тип операції', 'Опис', 'Вартість']
        widgets = [combo_flight, combo_type, entry_description, entry_cost]
        
        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)

        def save():
            # Перевірка рейсу
            if combo_flight.current() < 0:
                messagebox.showerror('Помилка', 'Оберіть рейс')
                return

            # Перевірка типу операції
            if not combo_type.get().strip():
                messagebox.showerror('Помилка', 'Оберіть тип операції')
                return

            # Перевірка вартості
            cost_str = entry_cost.get().strip()
            if not cost_str:
                messagebox.showerror('Помилка', 'Вкажіть вартість')
                return
            try:
                cost = float(cost_str)
                if cost < 0:
                    messagebox.showerror('Помилка', 'Вартість не може бути відʼємною')
                    return
            except ValueError:
                messagebox.showerror('Помилка', 'Вартість повинна бути числом')
                return

            # Опис (опційно, але можна перевірити на порожнечу)
            description = entry_description.get().strip()
            if not description:
                description = ''  # або можна вимагати введення

            flight_id = flights[combo_flight.current()]['id']

            # Виклик БД (для додавання або редагування)
            if db.add_airport_operation(flight_id, combo_type.get(), description, cost):  # для add
                messagebox.showinfo('Успіх', 'Аеропортну операцію додано')
                form.destroy()
                refresh()
            # Для редагування замінити на update_airport_operation(operation_id, ...)

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())
    
    def edit_airport_operation():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для редагування')
            return
        item = tree.item(sel[0])
        operation_id = item['values'][0]
        
        form = tk.Toplevel()
        form.title('Редагувати аеропортну операцію')
        flights = db.get_flights()
        combo_flight = ttk.Combobox(form, values=[f['flight_number'] for f in flights])
        combo_type = ttk.Combobox(form, values=['Прийом', 'Розвантаження', 'Зліт', 'Посадка', 'Диспетчерські послуги'])
        entry_description = tk.Entry(form)
        entry_cost = tk.Entry(form)

        # Встановлюємо поточні значення
        combo_type.set(item['values'][2])
        entry_description.insert(0, item['values'][3])
        entry_cost.insert(0, item['values'][4])

        # Встановлюємо рейс
        combo_flight.set(item['values'][1])

        labels = ['Рейс', 'Тип операції', 'Опис', 'Вартість']
        widgets = [combo_flight, combo_type, entry_description, entry_cost]
        
        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)

        def save():
            # Перевірка рейсу
            if combo_flight.current() < 0:
                messagebox.showerror('Помилка', 'Оберіть рейс')
                return

            # Перевірка типу операції
            if not combo_type.get().strip():
                messagebox.showerror('Помилка', 'Оберіть тип операції')
                return

            # Перевірка вартості
            cost_str = entry_cost.get().strip()
            if not cost_str:
                messagebox.showerror('Помилка', 'Вкажіть вартість')
                return
            try:
                cost = float(cost_str)
                if cost < 0:
                    messagebox.showerror('Помилка', 'Вартість не може бути відʼємною')
                    return
            except ValueError:
                messagebox.showerror('Помилка', 'Вартість повинна бути числом')
                return

            # Опис (опційно, але можна перевірити на порожнечу)
            description = entry_description.get().strip()
            if not description:
                description = ''  # або можна вимагати введення

            flight_id = flights[combo_flight.current()]['id']

            # Виклик БД (для додавання або редагування)
            # Виклик БД для редагування
            if db.update_airport_operation(operation_id, flight_id, combo_type.get(), description, cost):
                messagebox.showinfo('Успіх', 'Аеропортну операцію оновлено')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося оновити аеропортну операцію')

            # Для редагування замінити на update_airport_operation(operation_id, ...)

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())
    
    def delete_airport_operation():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити цю аеропортну операцію?'):
            operation_id = tree.item(sel[0])['values'][0]
            if db.delete_airport_operation(operation_id):
                messagebox.showinfo('Успіх', 'Аеропортну операцію видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити аеропортну операцію')
    
    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_airport_operation).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_airport_operation).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_airport_operation).pack(side='left')

# --- Митничні процедури ---
def show_customs_procedures_window():
    win = tk.Toplevel()
    win.title('Митничні процедури')
    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'Тип процедури', 'Опис', 'Статус', 'Дата'), show='headings')
    for col in ('ID', 'Турист', 'Тип процедури', 'Опис', 'Статус', 'Дата'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    def refresh():
        for i in tree.get_children(): tree.delete(i)
        tourists = {t['id']: t['full_name'] for t in db.get_tourists()}
        for cp in db.get_customs_procedures():
            tourist = tourists.get(cp['tourist_id'], '')
            tree.insert('', 'end', values=(cp['id'], tourist, cp['procedure_type'], cp['description'], cp['status'], cp['procedure_date']))
    refresh()
    def add_customs_procedure():
        form = tk.Toplevel()
        form.title('Додати митничну процедуру')
        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])
        combo_type = ttk.Combobox(form, values=['Декларація', 'Перевірка', 'Проблема'])
        entry_description = tk.Entry(form)
        combo_status = ttk.Combobox(form, values=['Завершено', 'В процесі', 'Проблема'])
        combo_status.set('Завершено')
        
        labels = ['Турист', 'Тип процедури', 'Опис', 'Статус']
        widgets = [combo_tourist, combo_type, entry_description, combo_status]
        
        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)
        
        def save():
            tourist_id = tourists[combo_tourist.current()]['id'] if combo_tourist.current() >= 0 else None
            if tourist_id and combo_type.get() and combo_status.get():
                if db.add_customs_procedure(tourist_id, combo_type.get(), entry_description.get(), combo_status.get()):
                    messagebox.showinfo('Успіх', 'Митничну процедуру додано')
                    form.destroy(); refresh()
                else:
                    messagebox.showerror('Помилка', 'Не вдалося додати митничну процедуру')
            else:
                messagebox.showerror('Помилка', 'Перевірте правильність введених даних')
        
        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())
    
    def edit_customs_procedure():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для редагування')
            return
        item = tree.item(sel[0])
        procedure_id = item['values'][0]
        
        form = tk.Toplevel()
        form.title('Редагувати митничну процедуру')
        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])
        combo_type = ttk.Combobox(form, values=['Декларація', 'Перевірка', 'Проблема'])
        entry_description = tk.Entry(form)
        combo_status = ttk.Combobox(form, values=['Завершено', 'В процесі', 'Проблема'])

        # Заповнити поточними значеннями
        current_tourist_name = item['values'][1]
        for idx, t in enumerate(tourists):
            if t['full_name'] == current_tourist_name:
                combo_tourist.current(idx)
                break

        # Заповнити поточними значеннями
        combo_type.set(item['values'][2])
        entry_description.insert(0, item['values'][3])
        combo_status.set(item['values'][4])
        
        labels = ['Турист', 'Тип процедури', 'Опис', 'Статус']
        widgets = [combo_tourist, combo_type, entry_description, combo_status]
        
        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)
        
        def save():
            tourist_id = tourists[combo_tourist.current()]['id'] if combo_tourist.current() >= 0 else None
            if tourist_id and combo_type.get() and combo_status.get():
                if db.update_customs_procedure(procedure_id, tourist_id, combo_type.get(), entry_description.get(), combo_status.get()):
                    messagebox.showinfo('Успіх', 'Митничну процедуру оновлено')
                    form.destroy(); refresh()
                else:
                    messagebox.showerror('Помилка', 'Не вдалося оновити митничну процедуру')
            else:
                messagebox.showerror('Помилка', 'Перевірте правильність введених даних')
        
        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())
    
    def delete_customs_procedure():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити цю митничну процедуру?'):
            procedure_id = tree.item(sel[0])['values'][0]
            if db.delete_customs_procedure(procedure_id):
                messagebox.showinfo('Успіх', 'Митничну процедуру видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити митничну процедуру')
    
    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_customs_procedure).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_customs_procedure).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_customs_procedure).pack(side='left')

# --- Публічні вікна для гостей ---
def show_hotel_public_window():
    win = tk.Toplevel()
    win.title('Готелі (публічний перегляд)')
    tree = ttk.Treeview(win, columns=('Назва', 'Адреса', 'К-сть номерів'), show='headings')
    for col in ('Назва', 'Адреса', 'К-сть номерів'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for h in db.get_hotels():
        tree.insert('', 'end', values=(h['name'], h['address'], h['rooms_count']))
    tk.Label(win, text='Публічна інформація - детальна інформація недоступна для гостей').pack()

def show_excursion_public_window():
    win = tk.Toplevel()
    win.title('Екскурсії (публічний перегляд)')
    tree = ttk.Treeview(win, columns=('Назва', 'Дата', 'Тривалість', 'Ціна'), show='headings')
    for col in ('Назва', 'Дата', 'Тривалість', 'Ціна'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for e in db.get_excursions():
        tree.insert('', 'end', values=(e['name'], e['date'], f"{e['duration']} год.", f"{e['price']} грн."))
    tk.Label(win, text='Публічна інформація - детальна інформація недоступна для гостей').pack()

def show_agency_public_window():
    win = tk.Toplevel()
    win.title('Агентства (публічний перегляд)')
    tree = ttk.Treeview(win, columns=('Назва', 'Контакти'), show='headings')
    for col in ('Назва', 'Контакти'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for a in db.get_excursion_agencies():
        tree.insert('', 'end', values=(a['name'], a['contact_info']))
    tk.Label(win, text='Публічна інформація - детальна інформація недоступна для гостей').pack()

# --- Функції валідації ---
def validate_number(value):
    """Перевіряє, чи є значення числом"""
    if not value:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_email(email):
    """Базова перевірка email"""
    return '@' in email and '.' in email

def validate_date(date_str):
    """Перевіряє формат дати YYYY-MM-DD"""
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_required(value):
    """Перевіряє, чи заповнене обов'язкове поле"""
    return value and value.strip()

if __name__ == '__main__':
    show_login_window()
