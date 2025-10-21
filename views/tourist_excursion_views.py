import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import queries as db


def show_tourist_excursion_window():
    win = tk.Toplevel()
    win.title('Туристи на екскурсіях')

    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'Екскурсія'), show='headings')
    for col in ('ID', 'Турист', 'Екскурсія'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        for te in db.get_tourist_excursions():
            tree.insert('', 'end', values=(te['id'], te['full_name'], te['excursion_name']))

    refresh()

    def add_tourist_excursion():
        form = tk.Toplevel()
        form.title('Додати туриста на екскурсію')

        # Отримуємо списки туристів та екскурсій
        tourists = db.get_tourists()
        excursions = db.get_excursions()

        tk.Label(form, text='Турист').grid(row=0, column=0)
        tourist_combo = ttk.Combobox(form, values=[f"{t['id']} - {t['full_name']}" for t in tourists])
        tourist_combo.grid(row=0, column=1)

        tk.Label(form, text='Екскурсія').grid(row=1, column=0)
        excursion_combo = ttk.Combobox(form, values=[f"{e['id']} - {e['name']} ({e['date']})" for e in excursions])
        excursion_combo.grid(row=1, column=1)

        def save():
            if tourist_combo.current() < 0 or excursion_combo.current() < 0:
                messagebox.showerror('Помилка', 'Оберіть туриста та екскурсію')
                return

            tourist_id = tourists[tourist_combo.current()]['id']
            excursion_id = excursions[excursion_combo.current()]['id']

            if db.add_tourist_excursion(tourist_id, excursion_id):
                messagebox.showinfo('Успіх', 'Туриста додано на екскурсію')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати туриста на екскурсію')

        tk.Button(form, text='Додати', command=save).grid(row=2, column=0, columnspan=2)

    def delete_tourist_excursion():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для видалення')
            return

        if messagebox.askyesno('Підтвердження', 'Видалити запис?'):
            record_id = tree.item(sel[0])['values'][0]
            if db.delete_tourist_excursion(record_id):
                messagebox.showinfo('Успіх', 'Запис видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити запис')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_tourist_excursion).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_tourist_excursion).pack(side='left')