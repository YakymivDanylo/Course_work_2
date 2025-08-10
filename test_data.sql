-- Тестові дані для перевірки роботи програми

-- Користувачі різних ролей
INSERT INTO keys (login, password, role) VALUES
('admin', 'admin123', 'Адміністратор'),
('operator1', 'op123', 'Оператор'),
('operator2', 'op456', 'Оператор'),
('authorized1', 'auth123', 'Авторизований'),
('authorized2', 'auth456', 'Авторизований'),
('guest1', 'guest123', 'Гість'),
('guest2', 'guest456', 'Гість')
ON CONFLICT (login) DO NOTHING;

-- Заявки від гостей
INSERT INTO requests (user_id, status, request_date) VALUES
((SELECT id FROM keys WHERE login = 'guest1'), 'Очікує', '2025-01-15'),
((SELECT id FROM keys WHERE login = 'guest2'), 'Схвалено', '2025-01-10')
ON CONFLICT DO NOTHING;

-- Туристи
INSERT INTO tourist (full_name, passport, gender, age, category, children_info) VALUES
('Іванов Іван Іванович', 'АА123456', 'чоловіча', 35, 'відпочинок', '2 діти'),
('Петрова Марія Петрівна', 'ВВ789012', 'жіноча', 28, 'відпочинок', '1 дитина'),
('Сидоров Олександр Васильович', 'СС345678', 'чоловіча', 42, 'вантаж', 'немає'),
('Коваленко Анна Сергіївна', 'DD901234', 'жіноча', 31, 'відпочинок', 'немає'),
('Мельник Віктор Ігорович', 'ЕЕ567890', 'чоловіча', 38, 'вантаж', 'немає'),
('Шевченко Олена Миколаївна', 'FF123789', 'жіноча', 25, 'відпочинок', 'немає'),
('Бондаренко Андрій Петрович', 'GG456123', 'чоловіча', 45, 'відпочинок', '3 діти'),
('Ткаченко Ірина Володимирівна', 'НН789456', 'жіноча', 33, 'вантаж', 'немає');

-- Готелі
INSERT INTO hotel (name, address, rooms_count, room_types) VALUES
('Гранд Отель', 'вул. Шевченка, 15, Київ', 150, 'стандарт, люкс, президентський'),
('Морський Бриз', 'вул. Приморська, 25, Одеса', 80, 'стандарт, люкс'),
('Карпатський Віктор', 'вул. Гірська, 10, Львів', 60, 'стандарт, люкс, сюїт'),
('Дніпровський', 'вул. Набережна, 5, Дніпро', 120, 'стандарт, люкс'),
('Харківський Центр', 'вул. Сумська, 20, Харків', 100, 'стандарт, люкс, президентський');

-- Екскурсійні агентства
INSERT INTO excursionagency (name, contact_info) VALUES
('ТурСвіт', 'тел: +380441234567, email: info@turswit.com'),
('Екскурсії Плюс', 'тел: +380481234567, email: info@excursionsplus.com'),
('Мандрівник', 'тел: +380321234567, email: info@mandrivnyk.com'),
('Туристичний Світ', 'тел: +380561234567, email: info@tourismworld.com'),
('Відпочинок Україна', 'тел: +380571234567, email: info@restukraine.com');

-- Екскурсії
INSERT INTO excursion (name, date, duration, agency_id, price) VALUES
('Київські святині', '2025-02-15', 4, (SELECT id FROM excursionagency WHERE name = 'ТурСвіт'), 500.00),
('Одеські катакомби', '2025-02-20', 3, (SELECT id FROM excursionagency WHERE name = 'Екскурсії Плюс'), 400.00),
('Львівська ратуша', '2025-02-25', 2, (SELECT id FROM excursionagency WHERE name = 'Мандрівник'), 300.00),
('Дніпровські кручі', '2025-03-01', 5, (SELECT id FROM excursionagency WHERE name = 'Туристичний Світ'), 600.00),
('Харківський зоопарк', '2025-03-05', 3, (SELECT id FROM excursionagency WHERE name = 'Відпочинок Україна'), 350.00),
('Київська лавра', '2025-03-10', 4, (SELECT id FROM excursionagency WHERE name = 'ТурСвіт'), 450.00),
('Одеський порт', '2025-03-15', 2, (SELECT id FROM excursionagency WHERE name = 'Екскурсії Плюс'), 250.00);

-- Вантаж
INSERT INTO cargo (tourist_id, places_count, weight, packing_cost, insurance, total) VALUES
((SELECT id FROM tourist WHERE full_name = 'Сидоров Олександр Васильович'), 5, 150.5, 200.00, 500.00, 850.00),
((SELECT id FROM tourist WHERE full_name = 'Мельник Віктор Ігорович'), 3, 80.2, 150.00, 300.00, 530.20),
((SELECT id FROM tourist WHERE full_name = 'Ткаченко Ірина Володимирівна'), 2, 45.8, 100.00, 200.00, 345.80),
((SELECT id FROM tourist WHERE full_name = 'Іванов Іван Іванович'), 1, 25.0, 50.00, 100.00, 175.00);

-- Візи
INSERT INTO visa (tourist_id, visa_number, issue_date, country, expiry_date) VALUES
((SELECT id FROM tourist WHERE full_name = 'Іванов Іван Іванович'), 'US123456', '2025-01-10', 'США', '2025-12-31'),
((SELECT id FROM tourist WHERE full_name = 'Петрова Марія Петрівна'), 'UK789012', '2025-01-15', 'Великобританія', '2025-12-31'),
((SELECT id FROM tourist WHERE full_name = 'Сидоров Олександр Васильович'), 'DE345678', '2025-01-20', 'Німеччина', '2025-12-31'),
((SELECT id FROM tourist WHERE full_name = 'Коваленко Анна Сергіївна'), 'FR901234', '2025-01-25', 'Франція', '2025-12-31'),
((SELECT id FROM tourist WHERE full_name = 'Мельник Віктор Ігорович'), 'IT567890', '2025-01-30', 'Італія', '2025-12-31'),
((SELECT id FROM tourist WHERE full_name = 'Шевченко Олена Миколаївна'), 'ES123789', '2025-02-05', 'Іспанія', '2025-12-31');

-- Групи туристів
INSERT INTO touristgroup (group_identifier, arrival_date, departure_date) VALUES
('GRP001', '2025-02-15', '2025-02-22'),
('GRP002', '2025-02-20', '2025-02-27'),
('GRP003', '2025-03-01', '2025-03-08'),
('GRP004', '2025-03-05', '2025-03-12'),
('GRP005', '2025-03-10', '2025-03-17');

-- Зв'язок туристів з групами
INSERT INTO touristgroupmember (group_id, tourist_id) VALUES
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP001'), (SELECT id FROM tourist WHERE full_name = 'Іванов Іван Іванович')),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP001'), (SELECT id FROM tourist WHERE full_name = 'Петрова Марія Петрівна')),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP002'), (SELECT id FROM tourist WHERE full_name = 'Сидоров Олександр Васильович')),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP002'), (SELECT id FROM tourist WHERE full_name = 'Коваленко Анна Сергіївна')),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP003'), (SELECT id FROM tourist WHERE full_name = 'Мельник Віктор Ігорович')),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP003'), (SELECT id FROM tourist WHERE full_name = 'Шевченко Олена Миколаївна')),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP004'), (SELECT id FROM tourist WHERE full_name = 'Бондаренко Андрій Петрович')),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP005'), (SELECT id FROM tourist WHERE full_name = 'Ткаченко Ірина Володимирівна'));

-- Зв'язок туристів з готелями
INSERT INTO touristhotel (tourist_id, hotel_id, checkin_date, checkout_date) VALUES
((SELECT id FROM tourist WHERE full_name = 'Іванов Іван Іванович'), (SELECT id FROM hotel WHERE name = 'Гранд Отель'), '2025-02-15', '2025-02-22'),
((SELECT id FROM tourist WHERE full_name = 'Петрова Марія Петрівна'), (SELECT id FROM hotel WHERE name = 'Морський Бриз'), '2025-02-20', '2025-02-27'),
((SELECT id FROM tourist WHERE full_name = 'Сидоров Олександр Васильович'), (SELECT id FROM hotel WHERE name = 'Карпатський Віктор'), '2025-03-01', '2025-03-08'),
((SELECT id FROM tourist WHERE full_name = 'Коваленко Анна Сергіївна'), (SELECT id FROM hotel WHERE name = 'Дніпровський'), '2025-03-05', '2025-03-12'),
((SELECT id FROM tourist WHERE full_name = 'Мельник Віктор Ігорович'), (SELECT id FROM hotel WHERE name = 'Харківський Центр'), '2025-03-10', '2025-03-17');

-- Зв'язок туристів з екскурсіями
INSERT INTO touristexcursion (tourist_id, excursion_id) VALUES
((SELECT id FROM tourist WHERE full_name = 'Іванов Іван Іванович'), (SELECT id FROM excursion WHERE name = 'Київські святині')),
((SELECT id FROM tourist WHERE full_name = 'Петрова Марія Петрівна'), (SELECT id FROM excursion WHERE name = 'Одеські катакомби')),
((SELECT id FROM tourist WHERE full_name = 'Сидоров Олександр Васильович'), (SELECT id FROM excursion WHERE name = 'Львівська ратуша')),
((SELECT id FROM tourist WHERE full_name = 'Коваленко Анна Сергіївна'), (SELECT id FROM excursion WHERE name = 'Дніпровські кручі')),
((SELECT id FROM tourist WHERE full_name = 'Мельник Віктор Ігорович'), (SELECT id FROM excursion WHERE name = 'Харківський зоопарк')),
((SELECT id FROM tourist WHERE full_name = 'Шевченко Олена Миколаївна'), (SELECT id FROM excursion WHERE name = 'Київська лавра')),
((SELECT id FROM tourist WHERE full_name = 'Бондаренко Андрій Петрович'), (SELECT id FROM excursion WHERE name = 'Одеський порт'));

-- Авіарейси
INSERT INTO flight (flight_number, date, seats_count, free_seats, cargo_weight, plane_class) VALUES
('PS123', '2025-02-15', 180, 45, 2500.5, 'Boeing 737'),
('PS124', '2025-02-20', 150, 30, 2000.0, 'Airbus A320'),
('PS125', '2025-03-01', 200, 60, 3000.0, 'Boeing 777'),
('PS126', '2025-03-05', 120, 25, 1500.5, 'Airbus A319'),
('PS127', '2025-03-10', 160, 40, 2200.0, 'Boeing 737'),
('PS128', '2025-03-15', 140, 35, 1800.0, 'Airbus A320'),
('PS129', '2025-03-20', 180, 50, 2500.0, 'Boeing 777');

-- Зв'язок туристів з авіарейсами
INSERT INTO touristflight (tourist_id, flight_id, arrival_date, departure_date) VALUES
((SELECT id FROM tourist WHERE full_name = 'Іванов Іван Іванович'), (SELECT id FROM flight WHERE flight_number = 'PS123'), '2025-02-15', '2025-02-22'),
((SELECT id FROM tourist WHERE full_name = 'Петрова Марія Петрівна'), (SELECT id FROM flight WHERE flight_number = 'PS124'), '2025-02-20', '2025-02-27'),
((SELECT id FROM tourist WHERE full_name = 'Сидоров Олександр Васильович'), (SELECT id FROM flight WHERE flight_number = 'PS125'), '2025-03-01', '2025-03-08'),
((SELECT id FROM tourist WHERE full_name = 'Коваленко Анна Сергіївна'), (SELECT id FROM flight WHERE flight_number = 'PS126'), '2025-03-05', '2025-03-12'),
((SELECT id FROM tourist WHERE full_name = 'Мельник Віктор Ігорович'), (SELECT id FROM flight WHERE flight_number = 'PS127'), '2025-03-10', '2025-03-17'),
((SELECT id FROM tourist WHERE full_name = 'Шевченко Олена Миколаївна'), (SELECT id FROM flight WHERE flight_number = 'PS128'), '2025-03-15', '2025-03-22'),
((SELECT id FROM tourist WHERE full_name = 'Бондаренко Андрій Петрович'), (SELECT id FROM flight WHERE flight_number = 'PS129'), '2025-03-20', '2025-03-27');

-- Фінансові звіти
INSERT INTO financialreport (group_id, income, expense_hotel, expense_transport, expense_excursion, expense_airport, expense_cargo) VALUES
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP001'), 15000.00, 5000.00, 2000.00, 1000.00, 500.00, 300.00),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP002'), 12000.00, 4000.00, 1500.00, 800.00, 400.00, 250.00),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP003'), 18000.00, 6000.00, 2500.00, 1200.00, 600.00, 400.00),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP004'), 14000.00, 4500.00, 1800.00, 900.00, 450.00, 280.00),
((SELECT id FROM touristgroup WHERE group_identifier = 'GRP005'), 16000.00, 5500.00, 2200.00, 1100.00, 550.00, 350.00);

-- Додаткові фінансові звіти без групи (для тестування)
INSERT INTO financialreport (group_id, income, expense_hotel, expense_transport, expense_excursion, expense_airport, expense_cargo) VALUES
(NULL, 25000.00, 8000.00, 3000.00, 1500.00, 800.00, 500.00),
(NULL, 30000.00, 10000.00, 3500.00, 1800.00, 900.00, 600.00);

-- Митничні процедури
INSERT INTO customs_procedures (tourist_id, procedure_type, description, status, procedure_date) VALUES
((SELECT id FROM tourist WHERE full_name = 'Іванов Іван Іванович' LIMIT 1), 'Декларація', 'Оформлення декларації', 'Завершено', '2025-01-15'),
((SELECT id FROM tourist WHERE full_name = 'Петрова Марія Петрівна' LIMIT 1), 'Перевірка', 'Перевірка багажу', 'Завершено', '2025-01-16'),
((SELECT id FROM tourist WHERE full_name = 'Сидоров Олександр Васильович' LIMIT 1), 'Проблема', 'Затримка через документи', 'В процесі', '2025-01-17');

INSERT INTO airport_operations (flight_id, operation_type, description, cost, operation_date) VALUES
((SELECT id FROM flight WHERE flight_number = 'PS123' LIMIT 1), 'Прийом', 'Прийом пасажирів', 1000.00, '2025-02-15'),
((SELECT id FROM flight WHERE flight_number = 'PS124' LIMIT 1), 'Розвантаження', 'Розвантаження багажу', 1500.00, '2025-02-20'),
((SELECT id FROM flight WHERE flight_number = 'PS125' LIMIT 1), 'Зліт', 'Підготовка до зльоту', 1200.00, '2025-03-01');

INSERT INTO weight_list (cargo_id, item_description, weight, marking, packaging_type, created_date) VALUES
((SELECT id FROM cargo WHERE tourist_id = (SELECT id FROM tourist WHERE full_name = 'Сидоров Олександр Васильович' LIMIT 1) LIMIT 1), 'Вантаж 1', 50.5, 'Маркування 1', 'Пакування 1', '2025-01-10'),
((SELECT id FROM cargo WHERE tourist_id = (SELECT id FROM tourist WHERE full_name = 'Мельник Віктор Ігорович' LIMIT 1) LIMIT 1), 'Вантаж 2', 30.0, 'Маркування 2', 'Пакування 2', '2025-01-11'),
((SELECT id FROM cargo WHERE tourist_id = (SELECT id FROM tourist WHERE full_name = 'Ткаченко Ірина Володимирівна' LIMIT 1) LIMIT 1), 'Вантаж 3', 20.0, 'Маркування 3', 'Пакування 3', '2025-01-12');