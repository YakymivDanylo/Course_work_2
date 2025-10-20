import tkinter as tk
from tkinter import ttk, messagebox
import re
from utils.validators import validate_required, validate_number
import queries as db


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

            if not validate_required(name):
                messagebox.showerror('Помилка', 'Назва готелю є обов\'язковою')
                return
            if name.isdigit():
                messagebox.showerror('Помилка', 'Назва готелю не може складатися лише з цифр')
                return

            if not validate_required(rooms):
                messagebox.showerror('Помилка', 'Поле "К-сть номерів" є обов\'язковим')
                return
            if not validate_number(rooms):
                messagebox.showerror('Помилка', 'Кількість номерів має бути числом')
                return

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

            if not validate_required(name):
                messagebox.showerror('Помилка', 'Назва готелю є обов\'язковою')
                return
            if name.isdigit():
                messagebox.showerror('Помилка', 'Назва готелю не може складатися лише з цифр')
                return

            if not validate_required(rooms):
                messagebox.showerror('Помилка', 'Поле "К-сть номерів" є обов\'язковим')
                return
            if not validate_number(rooms):
                messagebox.showerror('Помилка', 'Кількість номерів має бути числом')
                return

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