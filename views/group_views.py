import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import queries as db


def show_group_window():
    win = tk.Toplevel()
    win.title('Групи туристів')
    tree = ttk.Treeview(win, columns=('ID', 'Ідентифікатор', 'Дата прильоту', 'Дата відльоту'), show='headings')
    for col in ('ID', 'Ідентифікатор', 'Дата прильоту', 'Дата відльоту'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children(): tree.delete(i)
        for g in db.get_tourist_groups():
            tree.insert('', 'end', values=(g['id'], g['group_identifier'], g['arrival_date'], g['departure_date']))

    refresh()

    def add_group():
        form = tk.Toplevel()
        form.title('Додати групу')
        entry_id = tk.Entry(form)
        entry_arrival = DateEntry(form, date_pattern='yyyy-mm-dd')
        entry_departure = DateEntry(form, date_pattern='yyyy-mm-dd')
        tk.Label(form, text='Ідентифікатор').grid(row=0, column=0)
        entry_id.grid(row=0, column=1)
        tk.Label(form, text='Дата прильоту').grid(row=1, column=0)
        entry_arrival.grid(row=1, column=1)
        tk.Label(form, text='Дата відльоту').grid(row=2, column=0)
        entry_departure.grid(row=2, column=1)

        def save():
            if db.add_tourist_group(entry_id.get(), entry_arrival.get(), entry_departure.get()):
                messagebox.showinfo('Успіх', 'Групу додано')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати групу')

        tk.Button(form, text='Зберегти', command=save).grid(row=3, column=0, columnspan=2)

    tk.Button(win, text='Додати', command=add_group).pack()


def show_group_members_window():
    win = tk.Toplevel()
    win.title('Учасники груп')

    tree = ttk.Treeview(win, columns=('ID', 'Група', 'Турист', 'Паспорт'), show='headings')
    for col in ('ID', 'Група', 'Турист', 'Паспорт'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children():
            tree.delete(i)

        groups_dict = {g['id']: g['group_identifier'] for g in db.get_tourist_groups()}
        tourists_dict = {t['id']: t for t in db.get_tourists()}

        all_groups = db.get_tourist_groups()
        for group in all_groups:
            tourists_in_group = db.get_tourists_in_group(group['id'])
            for tourist in tourists_in_group:
                tree.insert('', 'end', values=(
                    f"{group['id']}-{tourist['id']}",
                    groups_dict.get(group['id'], ''),
                    tourist['full_name'],
                    tourist['passport']
                ))

    refresh()

    def add_member():
        form = tk.Toplevel()
        form.title('Додати туриста до групи')

        groups = db.get_tourist_groups()
        tourists = db.get_tourists()

        combo_group = ttk.Combobox(form, values=[g['group_identifier'] for g in groups])
        combo_tourist = ttk.Combobox(form, values=[t['full_name'] for t in tourists])

        tk.Label(form, text='Група').grid(row=0, column=0)
        combo_group.grid(row=0, column=1)
        tk.Label(form, text='Турист').grid(row=1, column=0)
        combo_tourist.grid(row=1, column=1)

        def save():
            group_index = combo_group.current()
            tourist_index = combo_tourist.current()

            group_id = groups[group_index]['id'] if group_index >= 0 else None
            tourist_id = tourists[tourist_index]['id'] if tourist_index >= 0 else None

            if group_id is None:
                messagebox.showwarning('Помилка', 'Оберіть групу')
                return
            if tourist_id is None:
                messagebox.showwarning('Помилка', 'Оберіть туриста')
                return

            all_groups = db.get_tourist_groups()
            for g in all_groups:
                tourists_in_group = db.get_tourists_in_group(g['id'])
                if any(t['id'] == tourist_id for t in tourists_in_group):
                    messagebox.showwarning('Помилка', f'Турист вже є в групі "{g["group_identifier"]}"')
                    return

            if db.add_tourist_to_group(group_id, tourist_id):
                messagebox.showinfo('Успіх', 'Туриста додано до групи')
                form.destroy()
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося додати туриста до групи')

        tk.Button(form, text='Зберегти', command=save).grid(row=2, column=0, columnspan=2)

    def remove_member():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning('Помилка', 'Оберіть запис для видалення')
            return

        item_values = tree.item(selected_item[0])['values']
        group_name = item_values[1]
        tourist_name = item_values[2]

        groups = db.get_tourist_groups()
        tourists = db.get_tourists()

        group_id = None
        tourist_id = None

        for group in groups:
            if group['group_identifier'] == group_name:
                group_id = group['id']
                break

        for tourist in tourists:
            if tourist['full_name'] == tourist_name:
                tourist_id = tourist['id']
                break

        if group_id is None or tourist_id is None:
            messagebox.showerror('Помилка', 'Не вдалося знайти групу або туриста')
            return

        result = messagebox.askyesno('Підтвердження',
                                     f'Видалити туриста "{tourist_name}" з групи "{group_name}"?')

        if result:
            if db.remove_tourist_from_group(group_id, tourist_id):
                messagebox.showinfo('Успіх', 'Туриста видалено з групи')
                refresh()
            else:
                messagebox.showerror('Помилка', 'Не вдалося видалити туриста з групи')

    button_frame = tk.Frame(win)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text='Додати', command=add_member).pack(side='left', padx=5)
    tk.Button(button_frame, text='Видалити', command=remove_member).pack(side='left', padx=5)


def show_group_view_window():
    win = tk.Toplevel()
    win.title('Перегляд груп туристів')
    tree = ttk.Treeview(win, columns=('ID', 'Ідентифікатор', 'Дата прильоту', 'Дата відльоту'), show='headings')
    for col in ('ID', 'Ідентифікатор', 'Дата прильоту', 'Дата відльоту'):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)
    for g in db.get_tourist_groups():
        tree.insert('', 'end', values=(g['id'], g['group_identifier'], g['arrival_date'], g['departure_date']))
    tk.Label(win, text='Режим перегляду - редагування недоступне').pack()