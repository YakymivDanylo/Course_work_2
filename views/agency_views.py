import tkinter as tk
from tkinter import ttk, messagebox
import re
from utils.validators import validate_required
import queries as db

def show_agency_window():
    win = tk.Toplevel()
    win.title('Агентства')

    tree = ttk.Treeview(win, columns=('ID', 'Назва', 'Контакти'), show='headings')
    for col in ('ID', 'Назва', 'Контакти'):
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    tree.pack(fill='both', expand=True, padx=10, pady=10)

    def get_all_agencies():
        return db.get_excursion_agencies()

    def is_name_unique(name, exclude_id=None):
        agencies = get_all_agencies()
        for agency in agencies:
            if exclude_id and agency['id'] == exclude_id:
                continue
            if agency['name'].strip().lower() == name.strip().lower():
                return False
        return True

    def extract_phone_and_email(contacts):
        contacts = contacts.strip()
        phone_pattern = re.compile(r'(\+?\d{10,13})')
        email_pattern = re.compile(r'([\w\.-]+@[\w\.-]+\.\w+)')

        phones = phone_pattern.findall(contacts)
        emails = email_pattern.findall(contacts)

        return phones, emails

    def are_contacts_unique(contacts, exclude_id=None):
        if not contacts.strip():
            return True, ""

        phones, emails = extract_phone_and_email(contacts)
        agencies = get_all_agencies()

        for agency in agencies:
            if exclude_id and agency['id'] == exclude_id:
                continue

            agency_phones, agency_emails = extract_phone_and_email(agency['contact_info'])

            for phone in phones:
                if phone in agency_phones:
                    return False, f"Телефон {phone} вже використовується"

            for email in emails:
                if email in agency_emails:
                    return False, f"Email {email} вже використовується"

        return True, ""

    def validate_contacts(value):
        value = value.strip()
        if not value:
            return False

        phone_pattern = re.compile(r'(\+?\d{10,13})')
        email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

        if phone_pattern.search(value) or email_pattern.search(value):
            return True
        return False

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        for a in db.get_excursion_agencies():
            tree.insert('', 'end', values=(a['id'], a['name'], a['contact_info']))

        win.update_idletasks()
        win.geometry(f"{tree.winfo_reqwidth() + 40}x{tree.winfo_reqheight() + 40}")

    refresh()

    def add_agency():
        form = tk.Toplevel()
        form.title('Додати агентство')
        labels = ['Назва', 'Контакти']
        entries = [tk.Entry(form) for _ in labels]

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            entries[i].grid(row=i, column=1)

        placeholder = "Телефон: ..., Email: ..."
        contacts_entry = entries[1]
        contacts_entry.insert(0, placeholder)
        contacts_entry.config(fg='grey')

        def on_focus_in(event):
            if contacts_entry.get() == placeholder:
                contacts_entry.delete(0, 'end')
                contacts_entry.config(fg='black')

        def on_focus_out(event):
            if not contacts_entry.get():
                contacts_entry.insert(0, placeholder)
                contacts_entry.config(fg='grey')

        contacts_entry.bind("<FocusIn>", on_focus_in)
        contacts_entry.bind("<FocusOut>", on_focus_out)

        def save():
            name = entries[0].get().strip()
            contacts = entries[1].get().strip()
            if contacts == placeholder:
                contacts = ""

            if not name:
                messagebox.showerror('Помилка', 'Заповніть назву агентства')
                return
            if not validate_contacts(contacts):
                messagebox.showerror('Помилка', 'Вкажіть хоча б телефон або email')
                return

            if not is_name_unique(name):
                messagebox.showerror('Помилка', 'Агентство з такою назвою вже існує')
                return

            contacts_unique, error_msg = are_contacts_unique(contacts)
            if not contacts_unique:
                messagebox.showerror('Помилка', error_msg)
                return

            if db.add_excursion_agency(name, contacts):
                messagebox.showinfo('Успіх', 'Агентство додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати агентство')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def edit_agency():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть агентство для редагування')
            return
        item = tree.item(sel[0])
        agency_id = item['values'][0]

        form = tk.Toplevel()
        form.title('Редагувати агентство')
        labels = ['Назва', 'Контакти']
        entries = [tk.Entry(form) for _ in labels]

        entries[0].insert(0, item['values'][1])
        entries[1].insert(0, item['values'][2])

        for i, l in enumerate(labels):
            tk.Label(form, text=l).grid(row=i, column=0)
            entries[i].grid(row=i, column=1)

        def save():
            name = entries[0].get().strip()
            contacts = entries[1].get().strip()

            if not name:
                messagebox.showerror('Помилка', 'Заповніть назву агентства')
                return
            if not validate_contacts(contacts):
                messagebox.showerror('Помилка', 'Вкажіть хоча б телефон або email')
                return

            if not is_name_unique(name, agency_id):
                messagebox.showerror('Помилка', 'Агентство з такою назвою вже існує')
                return

            contacts_unique, error_msg = are_contacts_unique(contacts, agency_id)
            if not contacts_unique:
                messagebox.showerror('Помилка', error_msg)
                return

            if db.update_excursion_agency(agency_id, name, contacts):
                messagebox.showinfo('Успіх', 'Агентство оновлено')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося оновити агентство')

        tk.Button(form, text='Зберегти', command=save).grid(row=len(labels), column=0, columnspan=2)
        form.bind('<Return>', lambda e: save())
        form.bind('<Escape>', lambda e: form.destroy())

    def delete_agency():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning('Попередження', 'Оберіть агентство для видалення')
            return
        if messagebox.askyesno('Підтвердження', 'Ви впевнені, що хочете видалити це агентство?'):
            agency_id = tree.item(sel[0])['values'][0]
            if db.delete_excursion_agency(agency_id):
                messagebox.showinfo('Успіх', 'Агентство видалено')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити агентство')

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')
    tk.Button(button_frame, text='Додати', command=add_agency).pack(side='left')
    tk.Button(button_frame, text='Редагувати', command=edit_agency).pack(side='left')
    tk.Button(button_frame, text='Видалити', command=delete_agency).pack(side='left')

def show_agency_view_window():
    win = tk.Toplevel()
    win.title('Перегляд агентств')
    tree = ttk.Treeview(win, columns=('ID', 'Назва', 'Контакти'), show='headings')
    for col in ('ID', 'Назва', 'Контакти'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for a in db.get_excursion_agencies():
        tree.insert('', 'end', values=(a['id'], a['name'], a['contact_info']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()

def show_agency_public_window():
    win = tk.Toplevel()
    win.title('Агентства (публічний перегляд)')
    tree = ttk.Treeview(win, columns=('Назва', 'Контакти'), show='headings')
    for col in ('Назва', 'Контакти'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for a in db.get_excursion_agencies():
        tree.insert('', 'end', values=(a['name'], a['contact_info']))
    tk.Label(win, text='Публічна інформація - детальна інформація недоступна для гостей').pack()