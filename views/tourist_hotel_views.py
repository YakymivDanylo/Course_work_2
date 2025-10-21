import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import queries as db


def show_tourist_hotel_window():
    win = tk.Toplevel()
    win.title('Туристи в готелях')

    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'Готель', 'Заселення', 'Виселення'), show='headings')
    for col in ('ID', 'Турист', 'Готель', 'Заселення', 'Виселення'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        for th in db.get_tourist_hotels():
            tree.insert('', 'end', values=(
                th['id'],
                th['full_name'],
                th['hotel_name'],
                th['checkin_date'],
                th['checkout_date']
            ))

    refresh()

    def add_tourist_hotel():
        form = tk.Toplevel()
        form.title('Додати туриста до готелю')

        tourists = db.get_tourists()
        hotels = db.get_hotels()

        tk.Label(form, text='Турист').grid(row=0, column=0)
        tourist_combo = ttk.Combobox(form, values=[f"{t['id']} - {t['full_name']}" for t in tourists])
        tourist_combo.grid(row=0, column=1)

        tk.Label(form, text='Готель').grid(row=1, column=0)
        hotel_combo = ttk.Combobox(form, values=[f"{h['id']} - {h['name']}" for h in hotels])
        hotel_combo.grid(row=1, column=1)

        tk.Label(form, text='Дата заселення').grid(row=2, column=0)
        checkin_date = DateEntry(form, date_pattern='yyyy-mm-dd')
        checkin_date.grid(row=2, column=1)

        tk.Label(form, text='Дата виселення').grid(row=3, column=0)
        checkout_date = DateEntry(form, date_pattern='yyyy-mm-dd')
        checkout_date.grid(row=3, column=1)

        def save():
            if tourist_combo.current() < 0 or hotel_combo.current() < 0:
                messagebox.showerror('Помилка', 'Оберіть туриста та готель')
                return

            tourist_id = tourists[tourist_combo.current()]['id']
            hotel_id = hotels[hotel_combo.current()]['id']

            if db.add_tourist_hotel(tourist_id, hotel_id, checkin_date.get(), checkout_date.get()):
                messagebox.showinfo('Успіх', 'Туриста додано до готелю')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати туриста до готелю')

        tk.Button(form, text='Додати', command=save).grid(row=4, column=0, columnspan=2)

    def delete_tourist_hotel():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для видалення')
            return

        if messagebox.askyesno('Підтвердження', 'Видалити запис?'):
            record_id = tree.item(sel[0])['values'][0]
            if db.delete_tourist_hotel(record_id):
                messagebox.showinfo('Успіх', 'Запис видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити запис')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_tourist_hotel).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_tourist_hotel).pack(side='left')