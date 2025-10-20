import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import queries as db


def show_flight_window():
    win = tk.Toplevel()
    win.title('Авіарейси')
    tree = ttk.Treeview(win, columns=('ID', 'Номер рейсу', 'Дата', 'К-сть місць', 'Вільні місця', 'Вага вантажу',
                                      'Клас літака'), show='headings')
    for col in ('ID', 'Номер рейсу', 'Дата', 'К-сть місць', 'Вільні місця', 'Вага вантажу', 'Клас літака'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children(): tree.delete(i)
        for f in db.get_flights():
            tree.insert('', 'end', values=(f['id'], f['flight_number'], f['date'], f['seats_count'], f['free_seats'],
                                           f['cargo_weight'], f['plane_class']))

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
            values = [w.get() for w in widgets]
            if any(v.strip() == '' for v in values):
                messagebox.showerror('Помилка', 'Усі поля мають бути заповнені!')
                return

            try:
                seats = int(entry_seats.get())
                free = int(entry_free.get())
                weight = float(entry_weight.get())
            except ValueError:
                messagebox.showerror('Помилка',
                                     'Поля "К-сть місць", "Вільні місця" та "Вага вантажу" мають містити тільки числа!')
                return

            if free > seats:
                messagebox.showerror('Помилка',
                                     'Кількість вільних місць не може перевищувати загальну кількість місць!')
                return

            if db.add_flight(entry_number.get(), entry_date.get(), seats, free, weight, entry_class.get()):
                messagebox.showinfo('Успіх', 'Авіарейс додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати авіарейс')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2, pady=10)

    tk.Button(win, text='Додати', command=add_flight).pack()


def show_flight_view_window():
    win = tk.Toplevel()
    win.title('Перегляд авіарейсів')
    tree = ttk.Treeview(win, columns=('ID', 'Номер рейсу', 'Дата', 'К-сть місць', 'Вільні місця', 'Вага вантажу',
                                      'Клас літака'), show='headings')
    for col in ('ID', 'Номер рейсу', 'Дата', 'К-сть місць', 'Вільні місця', 'Вага вантажу', 'Клас літака'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for f in db.get_flights():
        tree.insert('', 'end', values=(f['id'], f['flight_number'], f['date'], f['seats_count'], f['free_seats'],
                                       f['cargo_weight'], f['plane_class']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()