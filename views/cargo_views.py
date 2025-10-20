import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import validate_number
import queries as db


def show_cargo_window():
    win = tk.Toplevel()
    win.title('Вантаж')
    tree = ttk.Treeview(win,
                        columns=('ID', 'Турист', 'К-сть валіз', 'Вага(кг)', 'Вартість упаковки(грн)', 'Страховка(грн)',
                                 'Підсумок(грн)'), show='headings')
    for col in ('ID', 'Турист', 'К-сть валіз', 'Вага(кг)', 'Вартість упаковки(грн)', 'Страховка(грн)', 'Підсумок(грн)'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children(): tree.delete(i)
        tourists = {t['id']: t['full_name'] for t in db.get_tourists()}
        for c in db.get_cargos():
            tourist = tourists.get(c['tourist_id'], '')
            tree.insert('', 'end',
                        values=(c['id'], tourist, c['places_count'], c['weight'], c['packing_cost'], c['insurance'],
                                c['total']))

    refresh()

    def add_cargo():
        form = tk.Toplevel()
        form.title('Додати вантаж')

        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])

        labels = ['К-сть валіз', 'Вага', 'Вартість упаковки', 'Страховка', 'Підсумок']
        entries = [tk.Entry(form) for _ in labels]

        tk.Label(form, text='Турист').grid(row=0, column=0)
        combo_tourist.grid(row=0, column=1)

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i + 1, column=0)
            entries[i].grid(row=i + 1, column=1)

        entries[4].config(state='readonly')

        def calculate_total():
            try:
                count = int(entries[0].get())
                packing = float(entries[2].get())
                insurance = float(entries[3].get())
                total = count * (packing + insurance)
                entries[4].config(state='normal')
                entries[4].delete(0, tk.END)
                entries[4].insert(0, f"{total:.2f}")
                entries[4].config(state='readonly')
            except ValueError:
                entries[4].config(state='normal')
                entries[4].delete(0, tk.END)
                entries[4].insert(0, "0.00")
                entries[4].config(state='readonly')

        for i in [0, 2, 3]:
            entries[i].bind('<KeyRelease>', lambda e: calculate_total())

        def save():
            tourist_id = tourists[combo_tourist.current()]['id'] if combo_tourist.current() >= 0 else None
            if all(validate_number(e.get()) for e in entries[:4]) and tourist_id:
                if db.add_cargo(tourist_id, *(e.get() for e in entries)):
                    messagebox.showinfo('Успіх', 'Вантаж додано')
                    form.destroy()
                    refresh()
                else:
                    messagebox.showerror('Помилка', 'Не вдалося додати вантаж')
            else:
                messagebox.showerror('Помилка', 'Перевірте правильність введених даних')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels) + 1, column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_cargo():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть вантаж для редагування')
            return
        item = tree.item(sel[0])
        cargo_id = item['values'][0]

        form = tk.Toplevel()
        form.title('Редагувати вантаж')

        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])

        labels = ['К-сть валіз', 'Вага', 'Вартість упаковки', 'Страховка', 'Підсумок']
        entries = [tk.Entry(form) for _ in labels]

        combo_tourist.set(item['values'][1])
        for i, value in enumerate(item['values'][2:7]):
            entries[i].insert(0, str(value))

        tk.Label(form, text='Турист').grid(row=0, column=0)
        combo_tourist.grid(row=0, column=1)

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i + 1, column=0)
            entries[i].grid(row=i + 1, column=1)

        entries[4].config(state='readonly')

        def calculate_total():
            try:
                count = int(entries[0].get())
                packing = float(entries[2].get())
                insurance = float(entries[3].get())
                total = count * (packing + insurance)
                entries[4].config(state='normal')
                entries[4].delete(0, tk.END)
                entries[4].insert(0, f"{total:.2f}")
                entries[4].config(state='readonly')
            except ValueError:
                entries[4].config(state='normal')
                entries[4].delete(0, tk.END)
                entries[4].insert(0, "0.00")
                entries[4].config(state='readonly')

        for i in [0, 2, 3]:
            entries[i].bind('<KeyRelease>', lambda e: calculate_total())

        calculate_total()

        def save():
            tourist_id = tourists[combo_tourist.current()]['id'] if combo_tourist.current() >= 0 else None
            if all(validate_number(e.get()) for e in entries[:4]) and tourist_id:
                if db.update_cargo(cargo_id, tourist_id, *(e.get() for e in entries)):
                    messagebox.showinfo('Успіх', 'Вантаж оновлено')
                    form.destroy()
                    refresh()
                else:
                    messagebox.showerror('Помилка', 'Не вдалося оновити вантаж')
            else:
                messagebox.showerror('Помилка', 'Перевірте правильність введених даних')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels) + 1, column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_cargo():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть вантаж для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити цей вантаж?'):
            cargo_id = tree.item(sel[0])['values'][0]
            if db.delete_cargo(cargo_id):
                messagebox.showinfo('Успіх', 'Вантаж видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити вантаж')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_cargo).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_cargo).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_cargo).pack(side='left')


def show_cargo_view_window():
    win = tk.Toplevel()
    win.title('Перегляд вантажу')
    tree = ttk.Treeview(win,
                        columns=('ID', 'Турист', 'К-сть місць', 'Вага', 'Вартість упаковки', 'Страховка', 'Підсумок'),
                        show='headings')
    for col in ('ID', 'Турист', 'К-сть місць', 'Вага', 'Вартість упаковки', 'Страховка', 'Підсумок'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    tourists = {t['id']: t['full_name'] for t in db.get_tourists()}
    for c in db.get_cargos():
        tourist = tourists.get(c['tourist_id'], '')
        tree.insert('', 'end',
                    values=(c['id'], tourist, c['places_count'], c['weight'], c['packing_cost'], c['insurance'],
                            c['total']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()