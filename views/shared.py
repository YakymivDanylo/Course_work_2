import tkinter as tk
from tkinter import ttk, messagebox
from utils.validators import validate_required, validate_number


def create_crud_window(title, columns, get_data_func, add_func=None, edit_func=None, delete_func=None):
    """Універсальна функція для створення CRUD вікон"""
    win = tk.Toplevel()
    win.title(title)

    tree = ttk.Treeview(win, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    def refresh():
        for i in tree.get_children():
            tree.delete(i)
        for item in get_data_func():
            tree.insert('', 'end', values=tuple(item.values()))

    refresh()

    button_frame = tk.Frame(win)
    button_frame.pack(fill='x')

    if add_func:
        tk.Button(button_frame, text='Додати', command=add_func).pack(side='left')
    if edit_func:
        tk.Button(button_frame, text='Редагувати', command=edit_func).pack(side='left')
    if delete_func:
        tk.Button(button_frame, text='Видалити', command=delete_func).pack(side='left')

    return win, tree, refresh