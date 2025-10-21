import tkinter as tk
from tkinter import messagebox
from models.current_user import current_user


def show_main_menu():
    # Локальний імпорт для уникнення циклічних залежностей
    from auth import logout, show_add_user_window, show_users_window
    from .tourist_views import show_tourist_window, show_tourist_view_window
    from .hotel_views import show_hotel_window, show_hotel_view_window, show_hotel_public_window
    from .excursion_views import show_excursion_window, show_excursion_view_window, show_excursion_public_window
    from .agency_views import show_agency_window, show_agency_view_window, show_agency_public_window
    from .cargo_views import show_cargo_window, show_cargo_view_window
    from .visa_views import show_visa_window, show_visa_view_window
    from .group_views import show_group_window, show_group_view_window, show_group_members_window
    from .flight_views import show_flight_window, show_flight_view_window
    from .financial_views import show_financial_window, show_financial_view_window, show_airport_operations_window, \
        show_customs_procedures_window
    from .query_views import show_queries_window
    from .request_views import show_requests_window
    from .tourist_excursion_views import show_tourist_excursion_window
    from .tourist_flight_views import show_tourist_flight_window
    from .tourist_hotel_views import show_tourist_hotel_window

    main_win = tk.Tk()
    main_win.title('Головне меню')
    main_win.attributes('-fullscreen', True)

    main_container = tk.Frame(main_win)
    main_container.pack(expand=True, fill='both')

    canvas = tk.Canvas(main_container)
    scrollbar = tk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    def configure_scrollable_frame(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind('<Configure>', configure_scrollable_frame)

    welcome_font = ('Arial', 18, 'bold')
    btn_font = ('Arial', 14)

    center_frame = tk.Frame(scrollable_frame)
    center_frame.pack(expand=True, fill='both')

    tk.Label(center_frame, text=f"Вітаємо, {current_user['login']} ({current_user['role']})", font=welcome_font).pack(
        pady=(0, 20))

    def create_button(text, command):
        return tk.Button(center_frame, text=text, font=btn_font, width=30, height=2, command=command)

    if current_user['role'] == 'Адміністратор':
        create_button('Додати користувача', show_add_user_window).pack(pady=5)
        create_button('Керування користувачами', show_users_window).pack(pady=5)

    if current_user['role'] in ['Оператор', 'Адміністратор']:
        create_button('Туристи', show_tourist_window).pack(pady=5)
        create_button('Готелі', show_hotel_window).pack(pady=5)
        create_button('Екскурсії', show_excursion_window).pack(pady=5)
        create_button('Агентства', show_agency_window).pack(pady=5)
        create_button('Вантаж', show_cargo_window).pack(pady=5)
        create_button('Візи', show_visa_window).pack(pady=5)
        create_button('Групи туристів', show_group_window).pack(pady=5)
        create_button('Туриста в групах', show_group_members_window).pack(pady=5)
        create_button('Авіарейси', show_flight_window).pack(pady=5)
        create_button('Фінансові звіти', show_financial_window).pack(pady=5)
        create_button('Аеропортні операції', show_airport_operations_window).pack(pady=5)
        create_button('Митничні процедури', show_customs_procedures_window).pack(pady=5)
        create_button('Туристи на екскурсіях', show_tourist_excursion_window).pack(pady=5)
        create_button('Туристи на рейсах', show_tourist_flight_window).pack(pady=5)
        create_button('Туристи в готелях', show_tourist_hotel_window).pack(pady=5)

    elif current_user['role'] == 'Авторизований':
        create_button('Переглянути туристів', show_tourist_view_window).pack(pady=5)
        create_button('Переглянути готелі', show_hotel_view_window).pack(pady=5)
        create_button('Переглянути екскурсії', show_excursion_view_window).pack(pady=5)
        create_button('Переглянути агентства', show_agency_view_window).pack(pady=5)
        create_button('Переглянути вантаж', show_cargo_view_window).pack(pady=5)
        create_button('Переглянути візи', show_visa_view_window).pack(pady=5)
        create_button('Переглянути групи', show_group_view_window).pack(pady=5)
        create_button('Переглянути авіарейси', show_flight_view_window).pack(pady=5)

    elif current_user['role'] == 'Гість':
        create_button('Переглянути готелі', show_hotel_public_window).pack(pady=5)
        create_button('Переглянути екскурсії', show_excursion_public_window).pack(pady=5)
        create_button('Переглянути агентства', show_agency_public_window).pack(pady=5)

    create_button('Функціональні запити', show_queries_window).pack(pady=5)
    create_button('Заявки', show_requests_window).pack(pady=5)
    create_button('Вийти', lambda: logout(main_win)).pack(pady=5)

    def on_key_press(event):
        if event.keysym == 'F1':
            messagebox.showinfo('Довідка',
                                'Клавішні комбінації:\n'
                                'F1 - Довідка\n'
                                'Escape - Закрити вікно\n'
                                'Enter - Підтвердити дію\n'
                                'Tab - Перехід до наступного поля\n'
                                'Shift+Tab - Перехід до попереднього поля')
        elif event.keysym == 'Escape':
            logout(main_win)

    main_win.bind('<KeyPress>', on_key_press)
    main_win.focus_set()

    def on_closing():
        logout(main_win)

    main_win.protocol("WM_DELETE_WINDOW", on_closing)
    main_win.mainloop()