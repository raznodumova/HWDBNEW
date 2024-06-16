import psycopg2

conn = psycopg2.connect(database='HWDBtest', user='postgres', password='5728821q')#объект подключения

first_name = input('Введите имя: ')
last_name = input('Введите фамилию: ')
email = input('Введите почту: ')
phone= input('Введите номер телефона: ')

first_name_raname = input('Введите имя, на которое заменить: ')
last_name_rename = input('Введите фамилию,на которую заменить: ')
email_rename = input('Введите почту, на которую заменить: ')
phone_rename = input('Введите номер телефона, на который заменить: ')

fall_str = ''


def create_table(conn): #создание структуры БД
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone_number;
        DROP TABLE users;
        """)
        conn.commit()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
        );
        """)
        conn.commit()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(255),
        users_id INTEGER REFERENCES users(id)
        );
        """)
        conn.commit()


def add_user(conn, first_name, last_name, email, phone=None): #Добавление нового клиента
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO users(first_name, last_name, email)
        VALUES (%s, %s, %s) RETURNING first_name, last_name, email;
        """, (first_name, last_name, email))
        print(cur.fetchone())


def add_phone(conn, phone): #Добавление номера телефона существующего клиента
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone_number(phone_number, users_id)
        VALUES (%s, %s) RETURNING phone_number, users_id;
        """, (phone, 1))
        print(cur.fetchone())


def change_user(conn, client_id):
    with conn.cursor() as cur:
        if first_name_raname:
            cur.execute("UPDATE users SET first_name = %s WHERE id = %s", (first_name_raname, client_id))
            conn.commit()
        else:
            cur.execute("UPDATE users SET first_name = %s WHERE id = %s", (first_name, client_id))
            conn.commit()
        if last_name_rename:
            cur.execute("UPDATE users SET last_name = %s WHERE id = %s", (last_name_rename, client_id))
            conn.commit()
        else:
            cur.execute("UPDATE users SET last_name = %s WHERE id = %s", (last_name, client_id))
            conn.commit()
        if email_rename:
            cur.execute("UPDATE users SET email = %s WHERE id = %s", (email_rename, client_id))
            conn.commit()
        else:
            cur.execute("UPDATE users SET email = %s WHERE id = %s", (email, client_id))
            conn.commit()
        if phone_rename:
            cur.execute("UPDATE phone_number SET phone_number = %s WHERE users_id = %s", (phone_rename, client_id))
            conn.commit()
        else:
            cur.execute("UPDATE phone_number SET phone_number = %s WHERE users_id = %s", (phone, client_id))
            conn.commit()


def delete_phone(conn, client_id, phone_number): #Удаление номера телефона
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number
        WHERE users_id = %s AND phone_number = %s;
        """, (client_id, phone_number))
        conn.commit()
        print('Телефон удален :(')


def find_user(conn, first_name='%', last_name='%', email='%', phone='%'):
    with conn.cursor() as cur:
        query = f"""
        SELECT us.first_name, us.last_name, us.email, ph.phone_number
        FROM users us
        LEFT JOIN phone_number ph ON us.id = ph.users_id
        WHERE us.first_name LIKE %(first_name)s OR us.last_name LIKE %(last_name)s OR us.email LIKE %(email)s OR ph.phone_number LIKE %(phone)s;
        """
        cur.execute(query, {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone})
        conn.commit()
        print(cur.fetchall())
        return cur.fetchall()


def delete_user(conn, users_id, id): #Удалить пользователя
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_number
        WHERE users_id = %s;
        DELETE FROM users
        WHERE id = %s;
        """, (users_id, id))
        conn.commit()
        print('Пользователь удален :(')


if __name__ == '__main__':
    create_table(conn)
    add_user(conn, first_name, last_name, email)
    add_phone(conn, phone)
    change_user(conn, 1)
    delete_phone(conn, 1, phone)
    find_user(conn, first_name, last_name, email, phone)
    delete_user(conn, 1, 1)
    conn.close()
