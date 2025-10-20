import tkinter as tk
import re
from datetime import datetime

def parse_duration(duration_str):
    """Перетворює HH:MM у хвилини"""
    match = re.match(r'^([0-9]{1,2}):([0-5][0-9])$', duration_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        return hours * 60 + minutes
    return None

def format_duration(minutes):
    """Перетворює хвилини у HH:MM"""
    h = minutes // 60
    m = minutes % 60
    return f"{h:02}:{m:02}"

def add_placeholder(entry, placeholder):
    """Додає плейсхолдер до поля вводу"""
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