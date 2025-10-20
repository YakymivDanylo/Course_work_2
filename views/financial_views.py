import tkinter as tk
from tkinter import ttk, messagebox
import queries as db


def show_financial_window():
    win = tk.Toplevel()
    win.title('Фінансові звіти')
    tree = ttk.Treeview(win, columns=('ID', 'Група', 'Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж'),
                        show='headings')
    for col in ('ID', 'Група', 'Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children(): tree.delete(i)
        groups = {g['id']: g['group_identifier'] for g in db.get_tourist_groups()}
        for f in db.get_financial_reports():
            group = groups.get(f['group_id'], '')
            tree.insert('', 'end', values=(f['id'], group, f['income'], f['expense_hotel'], f['expense_transport'],
                                           f['expense_excursion'], f['expense_airport'], f['expense_cargo']))

    refresh()

    def add_financial():
        form = tk.Toplevel()
        form.title('Додати фінансовий звіт')
        groups = db.get_tourist_groups()
        combo_group = ttk.Combobox(form, values=[g['group_identifier'] for g in groups])
        labels = ['Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж']
        entries = [tk.Entry(form) for _ in labels]
        tk.Label(form, text='Група').grid(row=0, column=0)
        combo_group.grid(row=0, column=1)
        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i + 1, column=0)
            entries[i].grid(row=i + 1, column=1)

        def save():
            if combo_group.current() < 0:
                messagebox.showerror('Помилка', 'Оберіть групу')
                return

            values = []
            labels_ua = ['Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж']

            for i, e in enumerate(entries):
                val = e.get().strip()
                if not val:
                    messagebox.showerror('Помилка', f'Поле "{labels_ua[i]}" не може бути порожнім')
                    return
                try:
                    num = float(val)
                    if num < 0:
                        messagebox.showerror('Помилка', f'Поле "{labels_ua[i]}" не може бути відʼємним')
                        return
                    values.append(num)
                except ValueError:
                    messagebox.showerror('Помилка', f'Поле "{labels_ua[i]}" повинно бути числом')
                    return

            group_id = groups[combo_group.current()]['id']

            if db.add_financial_report(group_id, *values):
                messagebox.showinfo('Успіх', 'Звіт додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати звіт')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels) + 1, column=0, columnspan=2)

    tk.Button(win, text='Додати', command=add_financial).pack()


def show_financial_view_window():
    win = tk.Toplevel()
    win.title('Перегляд фінансових звітів')
    tree = ttk.Treeview(win, columns=('ID', 'Група', 'Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж'),
                        show='headings')
    for col in ('ID', 'Група', 'Дохід', 'Готель', 'Транспорт', 'Екскурсії', 'Аеропорт', 'Вантаж'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    groups = {g['id']: g['group_identifier'] for g in db.get_tourist_groups()}
    for f in db.get_financial_reports():
        group = groups.get(f['group_id'], '')
        tree.insert('', 'end', values=(f['id'], group, f['income'], f['expense_hotel'], f['expense_transport'],
                                       f['expense_excursion'], f['expense_airport'], f['expense_cargo']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()


def show_airport_operations_window():
    win = tk.Toplevel()
    win.title('Аеропортні операції')
    tree = ttk.Treeview(win, columns=('ID', 'Рейс', 'Тип операції', 'Опис', 'Вартість(грн)', 'Дата'), show='headings')
    for col in ('ID', 'Рейс', 'Тип операції', 'Опис', 'Вартість(грн)', 'Дата'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children(): tree.delete(i)
        flights = {f['id']: f['flight_number'] for f in db.get_flights()}
        for op in db.get_airport_operations():
            flight = flights.get(op['flight_id'], '')
            tree.insert('', 'end', values=(op['id'], flight, op['operation_type'], op['description'], op['cost'],
                                           op['operation_date']))

    refresh()

    def add_airport_operation():
        form = tk.Toplevel()
        form.title('Додати аеропортну операцію')
        flights = db.get_flights()
        combo_flight = ttk.Combobox(form, values=[f['flight_number'] for f in flights])
        combo_type = ttk.Combobox(form, values=['Прийом', 'Розвантаження', 'Зліт', 'Посадка', 'Диспетчерські послуги'])
        entry_description = tk.Entry(form)
        entry_cost = tk.Entry(form)

        labels = ['Рейс', 'Тип операції', 'Опис', 'Вартість']
        widgets = [combo_flight, combo_type, entry_description, entry_cost]

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)

        def save():
            if combo_flight.current() < 0:
                messagebox.showerror('Помилка', 'Оберіть рейс')
                return

            if not combo_type.get().strip():
                messagebox.showerror('Помилка', 'Оберіть тип операції')
                return

            cost_str = entry_cost.get().strip()
            if not cost_str:
                messagebox.showerror('Помилка', 'Вкажіть вартість')
                return
            try:
                cost = float(cost_str)
                if cost < 0:
                    messagebox.showerror('Помилка', 'Вартість не може бути відʼємною')
                    return
            except ValueError:
                messagebox.showerror('Помилка', 'Вартість повинна бути числом')
                return

            description = entry_description.get().strip()
            if not description:
                description = ''

            flight_id = flights[combo_flight.current()]['id']

            if db.add_airport_operation(flight_id, combo_type.get(), description, cost):
                messagebox.showinfo('Успіх', 'Аеропортну операцію додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати аеропортну операцію')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_airport_operation():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для редагування')
            return
        item = tree.item(sel[0])
        operation_id = item['values'][0]

        form = tk.Toplevel()
        form.title('Редагувати аеропортну операцію')
        flights = db.get_flights()
        combo_flight = ttk.Combobox(form, values=[f['flight_number'] for f in flights])
        combo_type = ttk.Combobox(form, values=['Прийом', 'Розвантаження', 'Зліт', 'Посадка', 'Диспетчерські послуги'])
        entry_description = tk.Entry(form)
        entry_cost = tk.Entry(form)

        combo_type.set(item['values'][2])
        entry_description.insert(0, item['values'][3])
        entry_cost.insert(0, item['values'][4])
        combo_flight.set(item['values'][1])

        labels = ['Рейс', 'Тип операції', 'Опис', 'Вартість']
        widgets = [combo_flight, combo_type, entry_description, entry_cost]

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)

        def save():
            if combo_flight.current() < 0:
                messagebox.showerror('Помилка', 'Оберіть рейс')
                return

            if not combo_type.get().strip():
                messagebox.showerror('Помилка', 'Оберіть тип операції')
                return

            cost_str = entry_cost.get().strip()
            if not cost_str:
                messagebox.showerror('Помилка', 'Вкажіть вартість')
                return
            try:
                cost = float(cost_str)
                if cost < 0:
                    messagebox.showerror('Помилка', 'Вартість не може бути відʼємною')
                    return
            except ValueError:
                messagebox.showerror('Помилка', 'Вартість повинна бути числом')
                return

            description = entry_description.get().strip()
            if not description:
                description = ''

            flight_id = flights[combo_flight.current()]['id']

            if db.update_airport_operation(operation_id, flight_id, combo_type.get(), description, cost):
                messagebox.showinfo('Успіх', 'Аеропортну операцію оновлено')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося оновити аеропортну операцію')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_airport_operation():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити цю аеропортну операцію?'):
            operation_id = tree.item(sel[0])['values'][0]
            if db.delete_airport_operation(operation_id):
                messagebox.showinfo('Успіх', 'Аеропортну операцію видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити аеропортну операцію')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_airport_operation).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_airport_operation).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_airport_operation).pack(side='left')


def show_customs_procedures_window():
    win = tk.Toplevel()
    win.title('Митничні процедури')
    tree = ttk.Treeview(win, columns=('ID', 'Турист', 'Тип процедури', 'Опис', 'Статус', 'Дата'), show='headings')
    for col in ('ID', 'Турист', 'Тип процедури', 'Опис', 'Статус', 'Дата'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children(): tree.delete(i)
        tourists = {t['id']: t['full_name'] for t in db.get_tourists()}
        for cp in db.get_customs_procedures():
            tourist = tourists.get(cp['tourist_id'], '')
            tree.insert('', 'end', values=(cp['id'], tourist, cp['procedure_type'], cp['description'], cp['status'],
                                           cp['procedure_date']))

    refresh()

    def add_customs_procedure():
        form = tk.Toplevel()
        form.title('Додати митничну процедуру')
        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])
        combo_type = ttk.Combobox(form, values=['Декларація', 'Перевірка', 'Проблема'])
        entry_description = tk.Entry(form)
        combo_status = ttk.Combobox(form, values=['Завершено', 'В процесі', 'Проблема'])
        combo_status.set('Завершено')

        labels = ['Турист', 'Тип процедури', 'Опис', 'Статус']
        widgets = [combo_tourist, combo_type, entry_description, combo_status]

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)

        def save():
            tourist_id = tourists[combo_tourist.current()]['id'] if combo_tourist.current() >= 0 else None
            if tourist_id and combo_type.get() and combo_status.get():
                if db.add_customs_procedure(tourist_id, combo_type.get(), entry_description.get(), combo_status.get()):
                    messagebox.showinfo('Успіх', 'Митничну процедуру додано')
                    form.destroy()
                    refresh()
                else:
                    messagebox.showerror('Помилка', 'Не вдалося додати митничну процедуру')
            else:
                messagebox.showerror('Помилка', 'Перевірте правильність введених даних')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_customs_procedure():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для редагування')
            return
        item = tree.item(sel[0])
        procedure_id = item['values'][0]

        form = tk.Toplevel()
        form.title('Редагувати митничну процедуру')
        tourists = db.get_tourists()
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])
        combo_type = ttk.Combobox(form, values=['Декларація', 'Перевірка', 'Проблема'])
        entry_description = tk.Entry(form)
        combo_status = ttk.Combobox(form, values=['Завершено', 'В процесі', 'Проблема'])

        current_tourist_name = item['values'][1]
        for idx, t in enumerate(tourists):
            if t['full_name'] == current_tourist_name:
                combo_tourist.current(idx)
                break

        combo_type.set(item['values'][2])
        entry_description.insert(0, item['values'][3])
        combo_status.set(item['values'][4])

        labels = ['Турист', 'Тип процедури', 'Опис', 'Статус']
        widgets = [combo_tourist, combo_type, entry_description, combo_status]

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            widgets[i].grid(row=i, column=1)

        def save():
            tourist_id = tourists[combo_tourist.current()]['id'] if combo_tourist.current() >= 0 else None
            if tourist_id and combo_type.get() and combo_status.get():
                if db.update_customs_procedure(procedure_id, tourist_id, combo_type.get(), entry_description.get(),
                                               combo_status.get()):
                    messagebox.showinfo('Успіх', 'Митничну процедуру оновлено')
                    form.destroy()
                    refresh()
                else:
                    messagebox.showerror('Помилка', 'Не вдалося оновити митничну процедуру')
            else:
                messagebox.showerror('Помилка', 'Перевірте правильність введених даних')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_customs_procedure():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть запис для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити цю митничну процедуру?'):
            procedure_id = tree.item(sel[0])['values'][0]
            if db.delete_customs_procedure(procedure_id):
                messagebox.showinfo('Успіх', 'Митничну процедуру видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити митничну процедуру')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_customs_procedure).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_customs_procedure).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_customs_procedure).pack(side='left')