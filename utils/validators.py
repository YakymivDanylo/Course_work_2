from datetime import datetime

def validate_number(value):
    """Перевіряє, чи є значення числом"""
    if not value:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_email(email):
    """Базова перевірка email"""
    return '@' in email and '.' in email

def validate_date(date_str):
    """Перевіряє формат дати YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_required(value):
    """Перевіряє, чи заповнене обов'язкове поле"""
    return value and value.strip()