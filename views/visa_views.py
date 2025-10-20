import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import queries as db

def show_visa_window():
    win = tk.Toplevel()
    win.title('Візи')

    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'Номер', 'Дата видачі', 'Країна', 'Термін дії'), show='headings')
    for col in ('ID', 'Турист', 'Номер', 'Дата видачі', 'Країна', 'Термін дії'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        tourists_dict = {t['id']: t['full_name'] for t in db.get_tourists()}
        for v in db.get_visas():
            tourist = tourists_dict.get(v['tourist_id'], '')
            tree.insert('', 'end',
                        values=(v['id'], tourist, v['visa_number'], v['issue_date'], v['country'], v['expiry_date']))

    refresh()

    def add_visa():
        form = tk.Toplevel()
        form.title('Додати візу')

        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])
        entry_number = tk.Entry(form)
        entry_issue = DateEntry(form, date_pattern='yyyy-mm-dd')
        entry_country = tk.Entry(form)
        entry_expiry = DateEntry(form, date_pattern='yyyy-mm-dd')

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

        def save():
            tourist_index = combo_tourist.current()
            tourist_id = tourists[tourist_index]['id'] if tourist_index >= 0 else None

            issue_date = entry_issue.get()
            expiry_date = entry_expiry.get()
            visa_number = entry_number.get().strip()
            country = entry_country.get().strip()

            today = datetime.today().date()

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

            visas = db.get_visas()

            for v in visas:
                if v['tourist_id'] == tourist_id:
                    messagebox.showerror('Помилка', 'Цей турист вже має візу')
                    return

            for v in visas:
                if v['visa_number'].lower() == visa_number.lower():
                    messagebox.showerror('Помилка', 'Цей номер візи вже існує')
                    return

            if db.add_visa(tourist_id, visa_number, issue_date, country, expiry_date):
                messagebox.showinfo('Успіх', 'Візу додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати візу')

        tk.Button(form, text='Зберегти', command=save).grid(row=5, column=0, columnspan=2)

    tk.Button(win, text='Додати', command=add_visa).pack()

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