import sqlite3

# Константа для имени базы данных
CALORIES_DB_NAME = 'calories.db'

def initiate_calories_db():
    conn = sqlite3.connect(CALORIES_DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Calories (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        gender TEXT NOT NULL,
        age INTEGER NOT NULL,
        growth INTEGER NOT NULL,
        weight INTEGER NOT NULL,
        calories INTEGER NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def add_calories_data(user_id, gender, age, growth, weight, calories):
    conn = sqlite3.connect(CALORIES_DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Calories (user_id, gender, age, growth, weight, calories) VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, gender, age, growth, weight, calories))

    conn.commit()
    conn.close()