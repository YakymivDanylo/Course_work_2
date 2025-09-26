-- Створення таблиці keys (користувачі)
CREATE TABLE keys (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Адміністратор', 'Оператор', 'Авторизований', 'Гість'))
);

-- Таблиця заявок на підвищення прав
CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES keys(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'Очікує', -- Очікує, Схвалено, Відхилено
    request_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Турист
CREATE TABLE tourist (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    passport VARCHAR(50) NOT NULL UNIQUE,
    gender VARCHAR(10),
    age INTEGER,
    category VARCHAR(20) CHECK (category IN ('відпочинок', 'вантаж')),
    children_info TEXT,
    is_child BOOLEAN DEFAULT FALSE, -- Чи є дитиною
    parent_id INTEGER REFERENCES tourist(id), -- Батько/мати для дітей
    can_get_visa BOOLEAN DEFAULT TRUE, -- Чи може отримати візу
    can_checkin_alone BOOLEAN DEFAULT TRUE -- Чи може самостійно поселитися
);

-- Готель
CREATE TABLE hotel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    rooms_count INTEGER,
    room_types VARCHAR(100)
);

-- Екскурсійне агентство
CREATE TABLE excursionagency (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(200)
);

-- Екскурсія
CREATE TABLE excursion (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    duration INTEGER, -- у годинах
    agency_id INTEGER REFERENCES excursionagency(id) ON DELETE SET NULL,
    price NUMERIC(10,2),
    allows_children BOOLEAN DEFAULT TRUE -- Чи дозволена для дітей
);

-- Віза
CREATE TABLE visa (
    id SERIAL PRIMARY KEY,
    tourist_id INTEGER REFERENCES tourist(id) ON DELETE CASCADE,
    visa_number VARCHAR(50) NOT NULL,
    issue_date DATE NOT NULL,
    country VARCHAR(50) NOT NULL,
    expiry_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Активна', -- Активна, Відхилена, Проблема
    problem_description TEXT -- Опис проблеми з візою
);

-- Вантаж
CREATE TABLE cargo (
    id SERIAL PRIMARY KEY,
    tourist_id INTEGER REFERENCES tourist(id) ON DELETE CASCADE,
    places_count INTEGER,
    weight NUMERIC(10,2),
    packing_cost NUMERIC(10,2),
    insurance NUMERIC(10,2),
    total NUMERIC(10,2)
);

-- Вагова відомість
CREATE TABLE weight_list (
    id SERIAL PRIMARY KEY,
    cargo_id INTEGER REFERENCES cargo(id) ON DELETE CASCADE,
    item_description TEXT,
    weight NUMERIC(10,2),
    marking VARCHAR(50),
    packaging_type VARCHAR(50),
    created_date DATE DEFAULT CURRENT_DATE
);

-- Авіарейс
CREATE TABLE flight (
    id SERIAL PRIMARY KEY,
    flight_number VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    seats_count INTEGER,
    free_seats INTEGER,
    cargo_weight NUMERIC(10,2),
    plane_class VARCHAR(50)
);

-- Аеропортні операції
CREATE TABLE airport_operations (
    id SERIAL PRIMARY KEY,
    flight_id INTEGER REFERENCES flight(id) ON DELETE CASCADE,
    operation_type VARCHAR(50), -- Прийом, Розвантаження, Зліт, Посадка, Диспетчерські послуги
    description TEXT,
    cost NUMERIC(10,2),
    operation_date DATE DEFAULT CURRENT_DATE
);

-- Митничні процедури
CREATE TABLE customs_procedures (
    id SERIAL PRIMARY KEY,
    tourist_id INTEGER REFERENCES tourist(id) ON DELETE CASCADE,
    procedure_type VARCHAR(50), -- Декларація, Перевірка, Проблема
    description TEXT,
    status VARCHAR(20) DEFAULT 'Завершено',
    procedure_date DATE DEFAULT CURRENT_DATE
);

-- Група туристів
CREATE TABLE touristgroup (
    id SERIAL PRIMARY KEY,
    group_identifier VARCHAR(50) NOT NULL,
    arrival_date DATE,
    departure_date DATE
);

-- Зв'язок: Турист у групі
CREATE TABLE touristgroupmember (
    group_id INTEGER REFERENCES touristgroup(id) ON DELETE CASCADE,
    tourist_id INTEGER REFERENCES tourist(id) ON DELETE CASCADE,
    PRIMARY KEY (group_id, tourist_id)
);

-- Зв'язок: Турист-Готель
CREATE TABLE touristhotel (
    id SERIAL PRIMARY KEY,
    tourist_id INTEGER REFERENCES tourist(id) ON DELETE CASCADE,
    hotel_id INTEGER REFERENCES hotel(id) ON DELETE CASCADE,
    checkin_date DATE,
    checkout_date DATE
);

-- Зв'язок: Турист-Екскурсія
CREATE TABLE touristexcursion (
    id SERIAL PRIMARY KEY,
    tourist_id INTEGER REFERENCES tourist(id) ON DELETE CASCADE,
    excursion_id INTEGER REFERENCES excursion(id) ON DELETE CASCADE
);

-- Фінансовий звіт
CREATE TABLE financialreport (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES touristgroup(id) ON DELETE SET NULL,
    income NUMERIC(12,2),
    expense_hotel NUMERIC(12,2),
    expense_transport NUMERIC(12,2),
    expense_excursion NUMERIC(12,2),
    expense_airport NUMERIC(12,2),
    expense_cargo NUMERIC(12,2),
    expense_unexpected NUMERIC(12,2), -- Непередбачені витрати
    expense_customs NUMERIC(12,2), -- Митничні витрати
    expense_visa NUMERIC(12,2) -- Візові витрати
);

-- Зв'язок: Турист-Авіарейс
CREATE TABLE touristflight (
    id SERIAL PRIMARY KEY,
    tourist_id INTEGER REFERENCES tourist(id) ON DELETE CASCADE,
    flight_id INTEGER REFERENCES flight(id) ON DELETE CASCADE,
    arrival_date DATE,
    departure_date DATE
);

-- Додати адміністратора за замовчуванням
INSERT INTO keys (login, password, role)
VALUES ('admin', 'admin123', 'Адміністратор')
ON CONFLICT (login) DO NOTHING;

-- Обмеження для дітей
ALTER TABLE tourist ADD CONSTRAINT check_child_visa 
    CHECK (NOT (is_child = TRUE AND can_get_visa = TRUE));

ALTER TABLE tourist ADD CONSTRAINT check_child_checkin 
    CHECK (NOT (is_child = TRUE AND can_checkin_alone = TRUE));

ALTER TABLE tourist
ADD CONSTRAINT unique_passport UNIQUE (passport);
