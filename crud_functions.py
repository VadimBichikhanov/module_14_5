import sqlite3

# Константа для имени базы данных
DB_NAME = 'products.db'

def initiate_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        image TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
    )
    ''')

    # Проверка наличия записей в таблице Products
    cursor.execute('SELECT COUNT(*) FROM Products')
    count = cursor.fetchone()[0]

    if count == 0:
        # Добавление записей в таблицу Products
        products = [
            ("Apple", "Свежее яблоко", 100, "images/apple.jpg"),
            ("Banana", "Спелый банан", 200, "images/banana.jpg"),
            ("Orange", "Апельсин", 300, "images/orange.jpg"),
            ("Grapes", "Виноград", 400, "images/grapes.jpg")
        ]

        cursor.executemany('''
        INSERT INTO Products (title, description, price, image) VALUES (?, ?, ?, ?)
        ''', products)

    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    conn.close()
    return products

def add_user(username, email, age):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)
    ''', (username, email, age))

    conn.commit()
    conn.close()

def is_included(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()
    return user is not None