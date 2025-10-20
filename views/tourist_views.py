import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import validate_required, validate_number
import queries as db

def show_tourist_window():
    win = tk.Toplevel()
    win.title('Туристи')
    tree = ttk.Treeview(win, columns=('ID', 'ПІБ', 'Паспорт', 'Стать', 'Вік', 'Категорія', 'Діти'), show='headings')
    for col in ('ID', 'ПІБ', 'Паспорт', 'Стать', 'Вік', 'Категорія', 'Діти'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children(): tree.delete(i)
        for t in db.get_tourists():
            tree.insert('', 'end', values=(t['id'], t['full_name'], t['passport'], t['gender'], t['age'], t['category'],
                                           t['children_info']))

    refresh()

    def add_tourist():
        form = tk.Toplevel()
        form.title('Додати туриста')

        def validate_children_input(char):
            return char != '-'

        def add_placeholder(entry, placeholder):
            entry.insert(0, placeholder)
            entry.config(fg='grey')

            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg='black')

            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg='grey')

            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)

        tk.Label(form, text='ПІБ').grid(row=0, column=0)
        entry_name = tk.Entry(form, width=30)
        add_placeholder(entry_name, 'Введіть ПІБ')
        entry_name.grid(row=0, column=1)

        tk.Label(form, text='Паспорт').grid(row=1, column=0)
        entry_passport = tk.Entry(form, width=30)
        add_placeholder(entry_passport, 'AA123456')
        entry_passport.grid(row=1, column=1)

        tk.Label(form, text='Стать').grid(row=2, column=0)
        combo_gender = ttk.Combobox(form, values=['чоловіча', 'жіноча'], state='readonly', width=28)
        combo_gender.set('Оберіть стать')
        combo_gender.grid(row=2, column=1)

        tk.Label(form, text='Вік').grid(row=3, column=0)
        entry_age = tk.Entry(form, width=30)
        add_placeholder(entry_age, 'Введіть вік')
        entry_age.grid(row=3, column=1)

        tk.Label(form, text='Категорія').grid(row=4, column=0)
        combo_category = ttk.Combobox(form, values=['відпочинок', 'вантаж'], state='readonly', width=28)
        combo_category.set('Оберіть категорію')
        combo_category.grid(row=4, column=1)

        tk.Label(form, text='Діти').grid(row=5, column=0)
        vcmd = (form.register(validate_children_input), '%S')
        entry_children = tk.Entry(form, width=30, validate='key', validatecommand=vcmd)
        add_placeholder(entry_children, 'Інформація про дітей')
        entry_children.grid(row=5, column=1)

        def save():
            name = entry_name.get().strip()
            passport = entry_passport.get().strip()
            gender = combo_gender.get()
            age = entry_age.get().strip()
            category = combo_category.get()
            children = entry_children.get().strip()

            if not validate_required(name) or name == 'Введіть ПІБ':
                messagebox.showerror('Помилка', 'ПІБ є обов\'язковим')
                return

            name_words = name.split()
            if len(name_words) != 3:
                messagebox.showerror('Помилка', 'ПІБ повинен містити рівно 3 слова (Прізвище Ім\'я По-батькові)')
                return

            if not validate_required(passport) or passport == 'AA123456':
                messagebox.showerror('Помилка', 'Паспорт є обов\'язковим, перевірте чи правильно ви його вписали')
                return

            existing_tourists = db.get_tourists()
            passport_exists = False
            for tourist in existing_tourists:
                if tourist['passport'] == passport:
                    passport_exists = True
                    break

            if passport_exists:
                messagebox.showerror('Помилка', 'Турист з таким номером паспорта вже існує')
                return

            if not validate_number(age):
                messagebox.showerror('Помилка', 'Вік повинен бути числом')
                return

            age_num = int(age)
            if age_num <= 0:
                messagebox.showerror('Помилка', 'Вік повинен бути більшим за 0')
                return

            if gender not in ['чоловіча', 'жіноча']:
                messagebox.showerror('Помилка', 'Виберіть стать')
                return

            if category not in ['відпочинок', 'вантаж']:
                messagebox.showerror('Помилка', 'Виберіть категорію (відпочинок/вантаж)')
                return

            if children and children != 'Інформація про дітей':
                if children.isdigit():
                    children_num = int(children)
                    if children_num == 0:
                        children = 'немає'
            else:
                children = 'немає'

            if db.add_tourist(name, passport, gender, age, category, children):
                messagebox.showinfo('Успіх', 'Туриста додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати туриста')

        tk.Button(form, text='Зберегти', command=save).grid(row=6, column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_tourist():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть туриста для редагування')
            return

        item = tree.item(sel[0])
        tourist_id = item['values'][0]
        current_values = item['values'][1:7]

        form = tk.Toplevel()
        form.title('Редагувати туриста')

        def validate_children_input(char):
            return char != '-'

        tk.Label(form, text='ПІБ').grid(row=0, column=0)
        entry_name = tk.Entry(form, width=30)
        entry_name.insert(0, current_values[0])
        entry_name.grid(row=0, column=1)

        tk.Label(form, text='Паспорт').grid(row=1, column=0)
        entry_passport = tk.Entry(form, width=30)
        entry_passport.insert(0, current_values[1])
        entry_passport.grid(row=1, column=1)

        passport_error_label = tk.Label(form, text='', fg='red', font=('Arial', 8))
        passport_error_label.grid(row=2, column=1, sticky='w')

        def check_passport_unique(*args):
            passport = entry_passport.get().strip()
            current_passport = current_values[1]

            if passport == current_passport:
                passport_error_label.config(text='')
                return True

            if not passport:
                passport_error_label.config(text='')
                return False

            is_unique = db.check_passport_unique(passport, tourist_id)

            if not is_unique:
                passport_error_label.config(text='Паспорт вже існує в базі даних')
                return False
            else:
                passport_error_label.config(text='')
                return True

        entry_passport_var = tk.StringVar()
        entry_passport_var.set(current_values[1])
        entry_passport_var.trace('w', check_passport_unique)
        entry_passport.config(textvariable=entry_passport_var)

        tk.Label(form, text='Стать').grid(row=3, column=0)
        combo_gender = ttk.Combobox(form, values=['чоловіча', 'жіноча'], state='readonly', width=28)
        combo_gender.set(current_values[2] if current_values[2] in ['чоловіча', 'жіноча'] else 'Оберіть стать')
        combo_gender.grid(row=3, column=1)

        tk.Label(form, text='Вік').grid(row=4, column=0)
        entry_age = tk.Entry(form, width=30)
        entry_age.insert(0, current_values[3])
        entry_age.grid(row=4, column=1)

        tk.Label(form, text='Категорія').grid(row=5, column=0)
        combo_category = ttk.Combobox(form, values=['відпочинок', 'вантаж'], state='readonly', width=28)
        combo_category.set(current_values[4] if current_values[4] in ['відпочинок', 'вантаж'] else 'Оберіть категорію')
        combo_category.grid(row=5, column=1)

        tk.Label(form, text='Діти').grid(row=6, column=0)
        vcmd = (form.register(validate_children_input), '%S')
        entry_children = tk.Entry(form, width=30, validate='key', validatecommand=vcmd)
        children_value = current_values[5] if current_values[5] and current_values[5] != 'немає' else ''
        entry_children.insert(0, children_value)
        entry_children.grid(row=6, column=1)

        def save():
            if not check_passport_unique():
                messagebox.showerror('Помилка', 'Паспорт вже існує в базі даних')
                return

            name = entry_name.get().strip()
            passport = entry_passport.get().strip()
            gender = combo_gender.get()
            age = entry_age.get().strip()
            category = combo_category.get()
            children = entry_children.get().strip()

            if not validate_required(name):
                messagebox.showerror('Помилка', 'ПІБ є обов\'язковим')
                return

            name_words = name.split()
            if len(name_words) != 3:
                messagebox.showerror('Помилка', 'ПІБ повинен містити рівно 3 слова (Прізвище Ім\'я По-батькові)')
                return

            if not validate_required(passport):
                messagebox.showerror('Помилка', 'Паспорт є обов\'язковим')
                return

            if not validate_number(age):
                messagebox.showerror('Помилка', 'Вік повинен бути числом')
                return

            age_num = int(age)
            if age_num <= 0:
                messagebox.showerror('Помилка', 'Вік повинен бути більшим за 0')
                return

            if gender not in ['чоловіча', 'жіноча']:
                messagebox.showerror('Помилка', 'Виберіть стать')
                return

            if category not in ['відпочинок', 'вантаж']:
                messagebox.showerror('Помилка', 'Виберіть категорію (відпочинок/вантаж)')
                return

            if children:
                if children.isdigit():
                    children_num = int(children)
                    if children_num == 0:
                        children = 'немає'
            else:
                children = 'немає'

            result = db.update_tourist(tourist_id, name, passport, gender, age, category, children)

            if result is True:
                messagebox.showinfo('Успіх', 'Туриста оновлено')
                form.destroy()
                refresh()
            elif result == 'duplicate_passport':
                messagebox.showerror('Помилка', 'Турист з таким номером паспорта вже існує')
            else:
                messagebox.showerror('Помилка', 'Не вдалося оновити туриста')

        tk.Button(form, text='Зберегти', command=save).grid(row=7, column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_tourist():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть туриста для видалення')
            return
        if messagebox.askyesno('Підтвердження',
                               'Ви впевнені, що хочете видалити цього туриста? Це також видалить всі пов\'язані дані.'):
            tourist_id = tree.item(sel[0])['values'][0]
            if db.delete_tourist(tourist_id):
                messagebox.showinfo('Успіх', 'Туриста видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити туриста')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_tourist).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_tourist).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_tourist).pack(side='left')

def show_tourist_view_window():
    win = tk.Toplevel()
    win.title('Перегляд туристів')
    tree = ttk.Treeview(win, columns=('ID', 'ПІБ', 'Паспорт', 'Стать', 'Вік', 'Категорія', 'Діти'), show='headings')
    for col in ('ID', 'ПІБ', 'Паспорт', 'Стать', 'Вік', 'Категорія', 'Діти'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for t in db.get_tourists():
        tree.insert('', 'end', values=(t['id'], t['full_name'], t['passport'], t['gender'], t['age'], t['category'], t['children_info']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()