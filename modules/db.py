import sqlite3

FOLDER_PATH = "src/data.db"
#создаёт базу данных, если таковой не имеется
def bd_create():
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                res INTEGER DEFAULT 0,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                pw TEXT NOT NULL
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
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS offers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        uid INTEGER NOT NULL,
                        offer  TEXT NOT NULL
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS protocols (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 uid INTEGER NOT NULL,
                 protocol  TEXT NOT NULL
                 date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
         ''')

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admins (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         uid INTEGER NOT NULL,
                    )
                 ''')


#проверка существования пользователя
def name_exists(name):
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE name = ? LIMIT 1", (name,))
        return cursor.fetchone() is not None

#проверка существования админа
def admin_exists(id):
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM admins WHERE uid = ? LIMIT 1", (id,))
        return cursor.fetchone() is not None

#вход или регистрация нового пользователя. на выходе даёт ID пользователя
def signin(name, pw):
    error = "Пароль введён не верно"
    role = False
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        if name_exists(name):
            id = cursor.execute("""
                        SELECT id
                        FROM users
                        WHERE name = ?
                    """, (name,)).fetchone()
            real_pw = cursor.execute("""
                              SELECT pw
                              FROM users
                              WHERE name = ?
                          """, (pw,)).fetchone()
            if admin_exists(id): role = True
            if pw == real_pw: return id, role
            else: return error

def signup(name,pw):
    error = "Такое имя уже существует"
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        if name_exists(name): return error
        else:
            cursor.execute("""
                INSERT INTO users (name)
                VALUES (?)
            """, (name,))
            id = cursor.execute("""
                                    SELECT id
                                    FROM users
                                    WHERE name = ?
                                """, (name,)).fetchone()
            if id == 1:
                cursor.execute("""
                                INSERT INTO admin (uid)
                                        VALUES (?)
                                """, (id,))
            return id

#даёт массив с данными первой сотни рекордсменов
def records():
    with sqlite3.connect(FOLDER_PATH) as conn:
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
    with sqlite3.connect(FOLDER_PATH) as conn:
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
def res(result, id_user):
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                        INSERT INTO history (uid, res)
                        VALUES (?,?)
                    """, (id_user, result))
        old = cursor.execute("""
                    SELECT res FROM users WHERE id = ?
                """, (id_user,))
        row = old.fetchone()
        if row[0] < result:
            cursor.execute("""
                                UPDATE users SET res = ? WHERE id = ?
                            """, (result, id_user,))
#загружает в таблицу предлоежения пользователей
def offer(id, offer):
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                                INSERT INTO offers (uid, offer)
                                VALUES (?,?)
                            """, (id, offer,))

#даёт массив с предложения пользователей
def offers():
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT uid, offer,date FROM offers 
        """)
        rows = cursor.fetchall()
        return rows


# загружает в таблицу действия администраторов
def protocoling(id, protocol):
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
                                INSERT INTO protocols (uid, protocol)
                                VALUES (?,?)
                            """, (id, protocol,))


# даёт массив с действиями администраторов
def protocols():
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT uid, protocol, date FROM protocol
        """)
        rows = cursor.fetchall()
        return rows

#АДМИНИСТРАТИВНЫЕ ФУНКЦИИ

#Удаление пользователя. Кнопка удалить может быть как у админа, так и у обычного пользователя. Админ может удалить всех. Обычный пользователь только себя
def ban(id):
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM users
            WHERE id=? 
        """, (id,))
        cursor.execute("""
                    DELETE FROM history
                    WHERE uid=? 
                """, (id,))
        if admin_exists(id):
            cursor.execute("""
                                DELETE FROM admins
                                WHERE uid=? 
                            """, (id,))

#Удаление пользователя из админов
def demotion(id, admin_id):
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        if admin_id == 1:
            cursor.execute("""
                DELETE FROM admins
                WHERE id=? 
            """, (id,))

#Повышение пользователя до уровня админа
def promotion(id, admin_id):
    with sqlite3.connect(FOLDER_PATH) as conn:
        cursor = conn.cursor()
        if admin_id == 1:
            if not admin_exists(id):
                cursor.execute("""
                INSERT INTO admin (uid)
                        VALUES (?)
                """, (id,))
