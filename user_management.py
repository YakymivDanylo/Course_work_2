import tkinter as tk
from tkinter import messagebox
import hashlib
from models.current_user import clear_current_user
from auth import show_login_window
import queries as db


def logout():
    clear_current_user()

    for widget in tk._default_root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()

    if tk._default_root:
        tk._default_root.destroy()

    show_login_window()