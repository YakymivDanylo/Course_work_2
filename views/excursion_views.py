import tkinter as tk
from tkinter import ttk, messagebox
import re
from tkcalendar import DateEntry
from utils.helpers import parse_duration, format_duration
import queries as db


def show_excursion_window():
    win = tk.Toplevel()
    win.title('Екскурсії')
    tree = ttk.Treeview(win, columns=('ID', 'Назва', 'Дата', 'Тривалість', 'Агентство', 'Ціна(грн)'), show='headings')
    for col in ('ID', 'Назва', 'Дата', 'Тривалість', 'Агентство', 'Ціна(грн)'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

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

        entry_name.insert(0, item['values'][1])
        entry_date.set_date(item['values'][2])
        entry_duration.insert(0, item['values'][3])
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

            if not duration:
                messagebox.showerror('Помилка', 'Невірний формат тривалості! Використовуйте ГГ:ХХ')
                return

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