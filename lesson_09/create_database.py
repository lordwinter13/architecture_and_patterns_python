import sqlite3

from settings import DATABASE_NAME, DDL_INSTRUCTIONS

connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

try:
    with open(DDL_INSTRUCTIONS, 'r') as f:
        text = f.read()
    cursor.executescript(text)
except Exception as e:
    print(f'Ошибка создания базы данных: {e}')

cursor.close()
connection.close()
