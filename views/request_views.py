import tkinter as tk
from tkinter import ttk, messagebox
# 1. ЗМІНЕНИЙ ІМПОРТ
from models import current_user as current_user_model
import queries as db


def show_requests_window():
    win = tk.Toplevel()
    win.title('Заявки')
    tree = ttk.Treeview(win, columns=('ID', 'Користувач', 'Статус', 'Дата'), show='headings')
    for col in ('ID', 'Користувач', 'Статус', 'Дата'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children():
            tree.delete(i)

        # Отримуємо поточного користувача з імпортованого модуля
        user = current_user_model.current_user

        # Передаємо user_id та role у функцію get_requests
        for r in db.get_requests(user_id=user['id'], role=user['role']):
            tree.insert('', 'end', values=(r['id'], r['login'], r['status'], r['request_date']))

    refresh()

    # 2. ЗВЕРТАЄМОСЬ ЧЕРЕЗ МОДУЛЬ
    if current_user_model.current_user['role'] == 'Гість':
        def send_request():
            # 3. ТУТ ТАКОЖ
            if db.add_request(current_user_model.current_user['id']):
                messagebox.showinfo('Успіх', 'Заявку подано')
                win.destroy()
            else:
                messagebox.showerror('Помилка', 'Не вдалося подати заявку')

        tk.Button(win, text='Подати заявку', command=send_request).pack()

    # 4. І ТУТ
    if current_user_model.current_user['role'] == 'Адміністратор':
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
                win.destroy()
                show_requests_window()

        tk.Button(win, text='Схвалити', command=approve).pack(side='left')
        tk.Button(win, text='Відхилити', command=reject).pack(side='left')