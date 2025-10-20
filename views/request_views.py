import tkinter as tk
from tkinter import ttk, messagebox
from models.current_user import current_user
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
        for r in db.get_requests():
            tree.insert('', 'end', values=(r['id'], r['login'], r['status'], r['request_date']))

    refresh()

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
                win.destroy()
                show_requests_window()

        tk.Button(win, text='Схвалити', command=approve).pack(side='left')
        tk.Button(win, text='Відхилити', command=reject).pack(side='left')