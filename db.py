import sqlite3
#создаёт базу данных, если таковой не имеется
def bd_create():
    with sqlite3.connect('src/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                res INTEGER DEFAULT 0,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid INTEGER NOT NULL,
                res INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

#проверка существования пользователя
def name_exists(name):
    with sqlite3.connect('src/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE name = ? LIMIT 1", (name,))
        return cursor.fetchone() is not None

#вход или регистрация нового пользователя. на выходе даёт ID пользователя
def signin(name):
    with sqlite3.connect('src/data.db') as conn:
        cursor = conn.cursor()
        if not name_exists(name):
            cursor.execute("""
                INSERT INTO users (name)
                VALUES (?)
            """, (name,))
        id = cursor.execute("""
                    SELECT id
                    FROM users
                    WHERE name = ?
                """, (name,)).fetchone()
    return id

#даёт массив с данными первой сотни рекордсменов
def records():
    with sqlite3.connect('src/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, res, date FROM users 
            ORDER BY res DESC
            LIMIT 100
        """)
        rows = cursor.fetchall()
        return rows
#даёт личную историю игр
def history(id):
    with sqlite3.connect('src/data.db') as conn:
        cursor = conn.execute("""
            SELECT res, date 
            FROM history
            WHERE uid = ?
            ORDER BY res DESC
            LIMIT 100
        """, (id,))
        rows = cursor.fetchall()
        return rows

#загружает в таблицу новые данные по окончанию игры
def res(res, id):
    with sqlite3.connect('src/data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
                        INSERT INTO history (uid, res)
                        VALUES (?,?)
                    """, (id, res))
        old = cursor.execute("""
                    SELECT res FROM users WHERE id = ?
                """, (name,))
        row = old.fetchone()
        if row[0] < res:
            cursor.execute("""
                                UPDATE users SET res = ? WHERE id = ?
                            """, (res, id))