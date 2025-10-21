import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import queries as db


def show_tourist_flight_window():
    win = tk.Toplevel()
    win.title('Туристи на рейсах')

    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'Рейс', 'Дата рейсу', 'Прибуття', 'Відбуття'), show='headings')
    for col in ('ID', 'Турист', 'Рейс', 'Дата рейсу', 'Прибуття', 'Відбуття'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        for tf in db.get_tourist_flights():
            tree.insert('', 'end', values=(
                tf['id'],
                tf['full_name'],
                tf['flight_number'],
                tf['flight_date'],
                tf['arrival_date'],
                tf['departure_date']
            ))

    refresh()

    def add_tourist_flight():
        form = tk.Toplevel()
        form.title('Додати туриста на рейс')

        tourists = db.get_tourists()
        flights = db.get_flights()

        tk.Label(form, text='Турист').grid(row=0, column=0)
        tourist_combo = ttk.Combobox(form, values=[f"{t['id']} - {t['full_name']}" for t in tourists])
        tourist_combo.grid(row=0, column=1)

        tk.Label(form, text='Рейс').grid(row=1, column=0)
        flight_combo = ttk.Combobox(form, values=[f"{f['id']} - {f['flight_number']} ({f['date']})" for f in flights])
        flight_combo.grid(row=1, column=1)

        tk.Label(form, text='Дата прибуття').grid(row=2, column=0)
        arrival_date = DateEntry(form, date_pattern='yyyy-mm-dd')
        arrival_date.grid(row=2, column=1)

        tk.Label(form, text='Дата відбуття').grid(row=3, column=0)
        departure_date = DateEntry(form, date_pattern='yyyy-mm-dd')
        departure_date.grid(row=3, column=1)

        def save():
            if tourist_combo.current() < 0 or flight_combo.current() < 0:
                messagebox.showerror('Помилка', 'Оберіть туриста та рейс')
                return

            tourist_id = tourists[tourist_combo.current()]['id']
            flight_id = flights[flight_combo.current()]['id']

            if db.add_tourist_flight(tourist_id, flight_id, arrival_date.get(), departure_date.get()):
                messagebox.showinfo('Успіх', 'Туриста додано на рейс')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати туриста на рейс')

        tk.Button(form, text='Додати', command=save).grid(row=4, column=0, columnspan=2)

    def delete_tourist_flight():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для видалення')
            return

        if messagebox.askyesno('Підтвердження', 'Видалити запис?'):
            record_id = tree.item(sel[0])['values'][0]
            if db.delete_tourist_flight(record_id):
                messagebox.showinfo('Успіх', 'Запис видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити запис')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_tourist_flight).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_tourist_flight).pack(side='left')