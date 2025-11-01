import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
from models.current_user import current_user, set_current_user, clear_current_user
import queries as db


def show_login_window():
    def login():
        login_val = entry_login.get()
        password_val = entry_password.get()

        if not login_val or not password_val:
            messagebox.showerror('Помилка', 'Будь ласка, заповніть всі поля')
            return

        user = db.get_user_by_login(login_val)
        hashed_entered_password = hashlib.sha256(password_val.encode('utf-8')).hexdigest()

        print(f"Login attempt: {login_val}")
        print(f"Entered password hash: {hashed_entered_password}")
        if user:
            print(f"Stored password hash: {user['password']}")

        if user and user['password'] == hashed_entered_password:
            set_current_user(user)
            login_win.destroy()

            import importlib
            from views import main_menu
            importlib.reload(main_menu)
            main_menu.show_main_menu()
        else:
            messagebox.showerror('Помилка', 'Невірний логін або пароль')

    def forgot_password():
        login_val = entry_login.get().strip()

        if not login_val:
            messagebox.showerror('Помилка', 'Введіть логін для відновлення паролю')
            return

        user = db.get_user_by_login(login_val)

        if not user:
            messagebox.showerror('Помилка', 'Користувача з таким логіном не знайдено')
            return

        messagebox.showinfo('Відновлення паролю',
                            'Для відновлення паролю зверніться до адміністратора.\n\n'
                            f'Логін: {login_val}\n'
                            'Адміністратор зможе змінити ваш пароль без знання поточного.')

    for widget in tk._default_root.winfo_children() if tk._default_root else []:
        try:
            widget.destroy()
        except:
            pass

    if tk._default_root:
        try:
            tk._default_root.quit()
            tk._default_root.destroy()
        except:
            pass

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
            login_win.quit()
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
    combo_role.set('Гість')

    entry_login.grid(row=0, column=1, padx=5, pady=5)
    entry_password.grid(row=1, column=1, padx=5, pady=5)
    combo_role.grid(row=2, column=1, padx=5, pady=5)

    def add():
        login_val = entry_login.get()
        password_val = entry_password.get()
        role_val = combo_role.get()

        if not login_val or not password_val or not role_val:
            messagebox.showerror('Помилка', 'Будь ласка, заповніть всі поля')
            return

        if db.user_exists(login_val):
            messagebox.showerror('Помилка', 'Користувач з таким логіном вже існує')
            return

        hashed_password = hashlib.sha256(password_val.encode('utf-8')).hexdigest()

        if db.add_user(login_val, hashed_password, role_val):
            messagebox.showinfo('Успіх', 'Користувача додано')
            win.destroy()
        else:
            messagebox.showerror('Помилка', 'Не вдалося додати користувача')

    tk.Button(win, text='Додати', command=add).grid(row=3, column=0, columnspan=2, pady=10)


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
        combo_role = ttk.Combobox(form, values=['Адміністратор', 'Оператор', 'Авторизований', 'Гість'],
                                  state='readonly', width=28)
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

            if password_val:
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


def logout(parent_window=None):
    clear_current_user()

    if parent_window:
        parent_window.destroy()

    for widget in tk._default_root.winfo_children() if tk._default_root else []:
        try:
            widget.destroy()
        except:
            pass

    if tk._default_root:
        try:
            tk._default_root.quit()
            tk._default_root.destroy()
        except:
            pass

    show_login_window()