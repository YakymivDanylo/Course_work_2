import psycopg2
from psycopg2 import sql, extras

# --- Налаштування підключення ---
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'tour_agency',
    'user': 'postgres',
    'password': 'lkol2567',
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print('Помилка підключення до БД:', e)
        return None

# --- CRUD-функції для Туристів ---
def add_tourist(full_name, passport, gender, age, category, children_info):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO tourist (full_name, passport, gender, age, category, children_info)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (full_name, passport, gender, age, category, children_info))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання туриста:', e)
        return False
    finally:
        conn.close()

def get_tourists():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM tourist')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання туристів:', e)
        return []
    finally:
        conn.close()

def update_tourist(tourist_id, full_name, passport, gender, age, category, children_info):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE tourist SET full_name=%s, passport=%s, gender=%s, age=%s, category=%s, children_info=%s
                WHERE id=%s
            ''', (full_name, passport, gender, age, category, children_info, tourist_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення туриста:', e)
        return False
    finally:
        conn.close()

def delete_tourist(tourist_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM tourist WHERE id=%s', (tourist_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення туриста:', e)
        return False
    finally:
        conn.close()

# Update user without changing password

def update_user_without_password(user_id, login, role):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE keys SET login=%s, role=%s WHERE id=%s
            ''', (login, role, user_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення користувача без пароля:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Готелів ---
def add_hotel(name, address, rooms_count, room_types):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO hotel (name, address, rooms_count, room_types)
                VALUES (%s, %s, %s, %s)
            ''', (name, address, rooms_count, room_types))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання готелю:', e)
        return False
    finally:
        conn.close()

def get_hotels():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM hotel')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання готелів:', e)
        return []
    finally:
        conn.close()

def update_hotel(hotel_id, name, address, rooms_count, room_types):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE hotel SET name=%s, address=%s, rooms_count=%s, room_types=%s
                WHERE id=%s
            ''', (name, address, rooms_count, room_types, hotel_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення готелю:', e)
        return False
    finally:
        conn.close()

def delete_hotel(hotel_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM hotel WHERE id=%s', (hotel_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення готелю:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Екскурсійного агентства ---
def add_excursion_agency(name, contact_info):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO excursionagency (name, contact_info)
                VALUES (%s, %s)
            ''', (name, contact_info))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання агентства:', e)
        return False
    finally:
        conn.close()

def get_excursion_agencies():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM excursionagency')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання агентств:', e)
        return []
    finally:
        conn.close()

def update_excursion_agency(agency_id, name, contact_info):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE excursionagency SET name=%s, contact_info=%s
                WHERE id=%s
            ''', (name, contact_info, agency_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення агентства:', e)
        return False
    finally:
        conn.close()

def delete_excursion_agency(agency_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM excursionagency WHERE id=%s', (agency_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення агентства:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Екскурсій ---
def add_excursion(name, date, duration, agency_id, price):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO excursion (name, date, duration, agency_id, price)
                VALUES (%s, %s, %s, %s, %s)
            ''', (name, date, duration, agency_id, price))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання екскурсії:', e)
        return False
    finally:
        conn.close()

def get_excursions():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM excursion')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання екскурсій:', e)
        return []
    finally:
        conn.close()

def update_excursion(excursion_id, name, date, duration, agency_id, price):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE excursion SET name=%s, date=%s, duration=%s, agency_id=%s, price=%s
                WHERE id=%s
            ''', (name, date, duration, agency_id, price, excursion_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення екскурсії:', e)
        return False
    finally:
        conn.close()

def delete_excursion(excursion_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM excursion WHERE id=%s', (excursion_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення екскурсії:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Вантажу ---
def add_cargo(tourist_id, places_count, weight, packing_cost, insurance, total):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO cargo (tourist_id, places_count, weight, packing_cost, insurance, total)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (tourist_id, places_count, weight, packing_cost, insurance, total))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання вантажу:', e)
        return False
    finally:
        conn.close()

def get_cargos():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM cargo')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання вантажу:', e)
        return []
    finally:
        conn.close()

def update_cargo(cargo_id, tourist_id, places_count, weight, packing_cost, insurance, total):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE cargo SET tourist_id=%s, places_count=%s, weight=%s, packing_cost=%s, insurance=%s, total=%s
                WHERE id=%s
            ''', (tourist_id, places_count, weight, packing_cost, insurance, total, cargo_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення вантажу:', e)
        return False
    finally:
        conn.close()

def delete_cargo(cargo_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM cargo WHERE id=%s', (cargo_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення вантажу:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Віз ---
def add_visa(tourist_id, visa_number, issue_date, country, expiry_date):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO visa (tourist_id, visa_number, issue_date, country, expiry_date)
                VALUES (%s, %s, %s, %s, %s)
            ''', (tourist_id, visa_number, issue_date, country, expiry_date))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання візи:', e)
        return False
    finally:
        conn.close()

def get_visas():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM visa')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання віз:', e)
        return []
    finally:
        conn.close()

def update_visa(visa_id, tourist_id, visa_number, issue_date, country, expiry_date):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE visa SET tourist_id=%s, visa_number=%s, issue_date=%s, country=%s, expiry_date=%s
                WHERE id=%s
            ''', (tourist_id, visa_number, issue_date, country, expiry_date, visa_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення візи:', e)
        return False
    finally:
        conn.close()

def delete_visa(visa_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM visa WHERE id=%s', (visa_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення візи:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Груп туристів ---
def add_tourist_group(group_identifier, arrival_date, departure_date):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO touristgroup (group_identifier, arrival_date, departure_date)
                VALUES (%s, %s, %s)
            ''', (group_identifier, arrival_date, departure_date))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання групи:', e)
        return False
    finally:
        conn.close()

def get_tourist_groups():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM touristgroup')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання груп:', e)
        return []
    finally:
        conn.close()

def update_tourist_group(group_id, group_identifier, arrival_date, departure_date):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE touristgroup SET group_identifier=%s, arrival_date=%s, departure_date=%s
                WHERE id=%s
            ''', (group_identifier, arrival_date, departure_date, group_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення групи:', e)
        return False
    finally:
        conn.close()

def delete_tourist_group(group_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM touristgroup WHERE id=%s', (group_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення групи:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Фінансових звітів ---
def add_financial_report(group_id, income, expense_hotel, expense_transport, expense_excursion, expense_airport, expense_cargo):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO financialreport (group_id, income, expense_hotel, expense_transport, expense_excursion, expense_airport, expense_cargo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (group_id, income, expense_hotel, expense_transport, expense_excursion, expense_airport, expense_cargo))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання фін. звіту:', e)
        return False
    finally:
        conn.close()

def get_financial_reports():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM financialreport')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання фін. звітів:', e)
        return []
    finally:
        conn.close()

def update_financial_report(report_id, group_id, income, expense_hotel, expense_transport, expense_excursion, expense_airport, expense_cargo):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE financialreport SET group_id=%s, income=%s, expense_hotel=%s, expense_transport=%s, expense_excursion=%s, expense_airport=%s, expense_cargo=%s
                WHERE id=%s
            ''', (group_id, income, expense_hotel, expense_transport, expense_excursion, expense_airport, expense_cargo, report_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення фін. звіту:', e)
        return False
    finally:
        conn.close()

def delete_financial_report(report_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM financialreport WHERE id=%s', (report_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення фін. звіту:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Авіарейсів ---
def add_flight(flight_number, date, seats_count, free_seats, cargo_weight, plane_class):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO flight (flight_number, date, seats_count, free_seats, cargo_weight, plane_class)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (flight_number, date, seats_count, free_seats, cargo_weight, plane_class))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання рейсу:', e)
        return False
    finally:
        conn.close()

def get_flights():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM flight')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання рейсів:', e)
        return []
    finally:
        conn.close()

def update_flight(flight_id, flight_number, date, seats_count, free_seats, cargo_weight, plane_class):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE flight SET flight_number=%s, date=%s, seats_count=%s, free_seats=%s, cargo_weight=%s, plane_class=%s
                WHERE id=%s
            ''', (flight_number, date, seats_count, free_seats, cargo_weight, plane_class, flight_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення рейсу:', e)
        return False
    finally:
        conn.close()

def delete_flight(flight_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM flight WHERE id=%s', (flight_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення рейсу:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Keys (користувачі) ---
def get_user_by_login(login):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM keys WHERE login = %s', (login,))
            return cur.fetchone()
    except Exception as e:
        print('Помилка пошуку користувача:', e)
        return None
    finally:
        conn.close()


def user_exists(login):
    """Перевіряє, чи існує користувач з вказаним логіном"""
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT login FROM keys WHERE login = %s', (login,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print('Помилка перевірки користувача:', e)
        return True  # У разі помилки краще не дозволити додавання
    finally:
        conn.close()


# Оновлена функція add_user для більш безпечної роботи
def add_user(login, password, role):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            # Додаємо перевірку на унікальність (забійний захід)
            cur.execute('SELECT login FROM keys WHERE login = %s', (login,))
            if cur.fetchone():
                return False  # Користувач вже існує

            cur.execute('''
                        INSERT INTO keys (login, password, role)
                        VALUES (%s, %s, %s)
                        ''', (login, password, role))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання користувача:', e)
        return False
    finally:
        conn.close()

def get_all_users():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM keys')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання користувачів:', e)
        return []
    finally:
        conn.close()

def update_user(user_id, login, password, role):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE keys SET login=%s, password=%s, role=%s WHERE id=%s
            ''', (login, password, role, user_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення користувача:', e)
        return False
    finally:
        conn.close()

def delete_user(user_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM keys WHERE id=%s', (user_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення користувача:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Requests (заявки) ---
def add_request(user_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO requests (user_id) VALUES (%s)', (user_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання заявки:', e)
        return False
    finally:
        conn.close()

def get_requests():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('''
                SELECT requests.*, keys.login FROM requests JOIN keys ON requests.user_id = keys.id
            ''')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання заявок:', e)
        return []
    finally:
        conn.close()

def update_request_status(request_id, status):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('UPDATE requests SET status=%s WHERE id=%s', (status, request_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення статусу заявки:', e)
        return False
    finally:
        conn.close()

def delete_request(request_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM requests WHERE id=%s', (request_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення заявки:', e)
        return False
    finally:
        conn.close()

# --- Функціональні запити ---
# 1. Рентабельність представництва
def get_profitability():
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT SUM(income) AS total_income, 
                       SUM(expense_hotel + expense_transport + expense_excursion + expense_airport + expense_cargo) AS total_expense
                FROM financialreport
            ''')
            row = cur.fetchone()
            if row and row[1] and row[1] != 0:
                return row[0] / row[1]
            return None
    except Exception as e:
        print('Помилка обчислення рентабельності:', e)
        return None
    finally:
        conn.close()

# 2. Витрати та прибутки за період
def get_financial_by_period(date_from, date_to):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('''
                SELECT * FROM financialreport WHERE id IN (
                    SELECT id FROM financialreport WHERE group_id IN (
                        SELECT id FROM touristgroup WHERE arrival_date >= %s AND departure_date <= %s
                    )
                )
            ''', (date_from, date_to))
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання фін. звітів за період:', e)
        return []
    finally:
        conn.close()

# 3. Завантаження рейсу на дату
def get_flight_load_by_date(date):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('''
                SELECT * FROM flight WHERE date = %s
            ''', (date,))
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання завантаження рейсу:', e)
        return []
    finally:
        conn.close()

# 4. Кількість туристів, популярні екскурсії/агентства за період
def get_excursion_stats(date_from, date_to):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('''
                SELECT COUNT(DISTINCT te.tourist_id) AS tourists_count,
                       e.name AS excursion_name,
                       a.name AS agency_name,
                       COUNT(te.excursion_id) AS excursion_orders
                FROM touristexcursion te
                JOIN excursion e ON te.excursion_id = e.id
                JOIN excursionagency a ON e.agency_id = a.id
                WHERE e.date BETWEEN %s AND %s
                GROUP BY e.name, a.name
                ORDER BY excursion_orders DESC
            ''', (date_from, date_to))
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання статистики екскурсій:', e)
        return []
    finally:
        conn.close()

# 5. Вантажообіг за період
def get_cargo_stats(date_from, date_to):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('''
                SELECT COUNT(c.id) AS places_count, SUM(c.weight) AS total_weight, COUNT(DISTINCT f.id) AS flights_count, f.plane_class
                FROM cargo c
                JOIN tourist t ON c.tourist_id = t.id
                JOIN touristflight tf ON t.id = tf.tourist_id
                JOIN flight f ON tf.flight_id = f.id
                WHERE f.date BETWEEN %s AND %s
                GROUP BY f.plane_class
            ''', (date_from, date_to))
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання вантажообігу:', e)
        return []
    finally:
        conn.close()

# 6. Інформація про туриста
def get_tourist_info(tourist_id):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            # Кількість поїздок у країну, дати, готелі, екскурсії, вантаж
            cur.execute('''
                SELECT t.*, 
                    (SELECT COUNT(*) FROM visa v WHERE v.tourist_id = t.id) AS trips_count,
                    (SELECT array_agg(DISTINCT tf.arrival_date) FROM touristflight tf WHERE tf.tourist_id = t.id) AS arrivals,
                    (SELECT array_agg(DISTINCT tf.departure_date) FROM touristflight tf WHERE tf.tourist_id = t.id) AS departures,
                    (SELECT array_agg(DISTINCT h.name) FROM touristhotel th JOIN hotel h ON th.hotel_id = h.id WHERE th.tourist_id = t.id) AS hotels,
                    (SELECT array_agg(DISTINCT e.name) FROM touristexcursion te JOIN excursion e ON te.excursion_id = e.id WHERE te.tourist_id = t.id) AS excursions,
                    (SELECT array_agg(DISTINCT c.id) FROM cargo c WHERE c.tourist_id = t.id) AS cargos
                FROM tourist t WHERE t.id = %s
            ''', (tourist_id,))
            return cur.fetchone()
    except Exception as e:
        print('Помилка отримання інформації про туриста:', e)
        return None
    finally:
        conn.close()

# 7. Фінансовий звіт для групи туристів
def get_group_financial_report(group_id):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM financialreport WHERE group_id = %s', (group_id,))
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання фін. звіту групи:', e)
        return []
    finally:
        conn.close()

# 8. Список готелів із зайнятими номерами та туристами за період
def get_hotel_occupancy(date_from, date_to):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('''
                SELECT h.name, COUNT(DISTINCT th.tourist_id) AS tourists_count, COUNT(th.id) AS rooms_occupied
                FROM touristhotel th
                JOIN hotel h ON th.hotel_id = h.id
                WHERE th.checkin_date >= %s AND th.checkout_date <= %s
                GROUP BY h.name
            ''', (date_from, date_to))
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання зайнятих номерів:', e)
        return []
    finally:
        conn.close()

# 9. Список туристів для митниці (загалом та за категоріями)
def get_customs_tourists(category=None):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            if category:
                cur.execute('SELECT * FROM tourist WHERE category = %s', (category,))
            else:
                cur.execute('SELECT * FROM tourist')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання туристів для митниці:', e)
        return []
    finally:
        conn.close()

# 10. Список туристів, які відвідали країну за період
def get_tourists_by_period(date_from, date_to, category=None):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            if category:
                cur.execute('''
                    SELECT DISTINCT t.* FROM tourist t
                    JOIN touristflight tf ON t.id = tf.tourist_id
                    WHERE tf.arrival_date >= %s AND tf.departure_date <= %s AND t.category = %s
                ''', (date_from, date_to, category))
            else:
                cur.execute('''
                    SELECT DISTINCT t.* FROM tourist t
                    JOIN touristflight tf ON t.id = tf.tourist_id
                    WHERE tf.arrival_date >= %s AND tf.departure_date <= %s
                ''', (date_from, date_to))
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання туристів за період:', e)
        return []
    finally:
        conn.close()

# --- CRUD-функції для Вагових відомостей ---
def add_weight_list(cargo_id, item_description, weight, marking, packaging_type):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO weight_list (cargo_id, item_description, weight, marking, packaging_type)
                VALUES (%s, %s, %s, %s, %s)
            ''', (cargo_id, item_description, weight, marking, packaging_type))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання вагової відомості:', e)
        return False
    finally:
        conn.close()

def get_weight_lists():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM weight_list')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання вагових відомостей:', e)
        return []
    finally:
        conn.close()

def update_weight_list(weight_id, cargo_id, item_description, weight, marking, packaging_type):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE weight_list SET cargo_id=%s, item_description=%s, weight=%s, marking=%s, packaging_type=%s
                WHERE id=%s
            ''', (cargo_id, item_description, weight, marking, packaging_type, weight_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення вагової відомості:', e)
        return False
    finally:
        conn.close()

def delete_weight_list(weight_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM weight_list WHERE id=%s', (weight_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення вагової відомості:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Аеропортних операцій ---
def add_airport_operation(flight_id, operation_type, description, cost):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO airport_operations (flight_id, operation_type, description, cost)
                VALUES (%s, %s, %s, %s)
            ''', (flight_id, operation_type, description, cost))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання аеропортної операції:', e)
        return False
    finally:
        conn.close()

def get_airport_operations():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM airport_operations')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання аеропортних операцій:', e)
        return []
    finally:
        conn.close()

def update_airport_operation(operation_id, flight_id, operation_type, description, cost):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE airport_operations SET flight_id=%s, operation_type=%s, description=%s, cost=%s
                WHERE id=%s
            ''', (flight_id, operation_type, description, cost, operation_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення аеропортної операції:', e)
        return False
    finally:
        conn.close()

def delete_airport_operation(operation_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM airport_operations WHERE id=%s', (operation_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення аеропортної операції:', e)
        return False
    finally:
        conn.close()

# --- CRUD-функції для Митничних процедур ---
def add_customs_procedure(tourist_id, procedure_type, description, status):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO customs_procedures (tourist_id, procedure_type, description, status)
                VALUES (%s, %s, %s, %s)
            ''', (tourist_id, procedure_type, description, status))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка додавання митничної процедури:', e)
        return False
    finally:
        conn.close()

def get_customs_procedures():
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM customs_procedures')
            return cur.fetchall()
    except Exception as e:
        print('Помилка отримання митничних процедур:', e)
        return []
    finally:
        conn.close()

def update_customs_procedure(procedure_id, tourist_id, procedure_type, description, status):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE customs_procedures SET tourist_id=%s, procedure_type=%s, description=%s, status=%s
                WHERE id=%s
            ''', (tourist_id, procedure_type, description, status, procedure_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення митничної процедури:', e)
        return False
    finally:
        conn.close()

def delete_customs_procedure(procedure_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM customs_procedures WHERE id=%s', (procedure_id,))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка видалення митничної процедури:', e)
        return False
    finally:
        conn.close()

def update_user_role(user_id, new_role):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                UPDATE keys SET role=%s WHERE id=%s
            ''', (new_role, user_id))
            conn.commit()
        return True
    except Exception as e:
        print('Помилка оновлення ролі користувача:', e)
        return False
    finally:
        conn.close()

def get_request_by_id(request_id):
    conn = get_connection()
    if not conn:
        return None
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('SELECT * FROM requests WHERE id=%s', (request_id,))
            return cur.fetchone()
    except Exception as e:
        print('Error fetching request by id:', e)
        return None
    finally:
        conn.close()

# --- CRUD functions for touristgroupmember ---
def add_tourist_to_group(group_id, tourist_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO touristgroupmember (group_id, tourist_id) VALUES (%s, %s)
            ''', (group_id, tourist_id))
            conn.commit()
        return True
    except Exception as e:
        print('Error adding tourist to group:', e)
        return False
    finally:
        conn.close()

def get_tourists_in_group(group_id):
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cur:
            cur.execute('''
                SELECT t.* FROM tourist t
                JOIN touristgroupmember tg ON t.id = tg.tourist_id
                WHERE tg.group_id = %s
            ''', (group_id,))
            return cur.fetchall()
    except Exception as e:
        print('Error getting tourists in group:', e)
        return []
    finally:
        conn.close()

def remove_tourist_from_group(group_id, tourist_id):
    conn = get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute('''
                DELETE FROM touristgroupmember WHERE group_id = %s AND tourist_id = %s
            ''', (group_id, tourist_id))
            conn.commit()
        return True
    except Exception as e:
        print('Error removing tourist from group:', e)
        return False
    finally:
        conn.close()
