import psycopg2
from psycopg2 import sql


def create_database():
    conn = psycopg2.connect(
        database="clients_db",
        user="postgres",
        password="dREdd250299",

    )
    conn.autocommit = True
    cursor = conn.cursor()
    # cursor.execute("DROP DATABASE IF EXISTS clients_db")
    # cursor.execute("CREATE DATABASE clients_db")
    cursor.close()
    conn.close()



# Функция для создания таблицы
def create_table():
    conn = psycopg2.connect(database="clients_db", user="postgres", password="dREdd250299",)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phones TEXT[]
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления нового клиента
def add_client(first_name, last_name, email, phones=None):
    if phones is None:
        phones = []
    conn = psycopg2.connect(database="clients_db", user="postgres", password="dREdd250299")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO clients (first_name, last_name, email, phones)
        VALUES (%s, %s, %s, %s)
    ''', (first_name, last_name, email, phones))
    conn.commit()
    conn.close()

# Функция для добавления телефона для существующего клиента
def add_phone(client_id, phone):
    conn = psycopg2.connect(database="clients_db", user="postgres", password="dREdd250299")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clients
        SET phones = array_append(phones, %s)
        WHERE id = %s
    ''', (phone, client_id))
    conn.commit()
    conn.close()

# Функция для изменения данных о клиенте
def update_client(client_id, first_name=None, last_name=None, email=None):
    conn = psycopg2.connect(database="clients_db", user="postgres", password="dREdd250299")
    cursor = conn.cursor()
    update_query = []
    update_params = []
    if first_name:
        update_query.append("first_name = %s")
        update_params.append(first_name)
    if last_name:
        update_query.append("last_name = %s")
        update_params.append(last_name)
    if email:
        update_query.append("email = %s")
        update_params.append(email)
    if update_query:
        update_query_str = ", ".join(update_query)
        update_params.append(client_id)
        cursor.execute(f'''
            UPDATE clients
            SET {update_query_str}
            WHERE id = %s
        ''', tuple(update_params))
        conn.commit()
    conn.close()

# Функция для удаления телефона для существующего клиента
def delete_phone(client_id, phone):
    conn = psycopg2.connect(database="clients_db", user="postgres", password="dREdd250299")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE clients
        SET phones = array_remove(phones, %s)
        WHERE id = %s
    ''', (phone, client_id))
    conn.commit()
    conn.close()

# Функция для удаления существующего клиента
def delete_client(client_id):
    conn = psycopg2.connect(database="clients_db", user="postgres", password="dREdd250299")
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM clients
        WHERE id = %s
    ''', (client_id,))
    conn.commit()
    conn.close()

# Функция для поиска клиента по данным
def find_client(query):
    conn = psycopg2.connect(database="clients_db", user="postgres", password="dREdd250299")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM clients
        WHERE first_name = %s OR last_name = %s OR email = %s OR %s = ANY(phones)
    ''', (query, query, query, query))
    clients = cursor.fetchall()
    conn.close()
    return clients

# Создание структуры БД
create_database()

# Создание таблицы
create_table()

# Добавление клиентов
add_client('Иван', 'Иванов', 'ivan@example.com', ['123456789', '987654321'])
add_client('Петр', 'Петров', 'petr@example.com', ['555555555'])

# Добавление телефонов для клиентов
add_phone(1, '999999999')

# Изменение данных о клиенте
update_client(2, email='new_petr@example.com')

# Удаление телефона для клиента
delete_phone(1, '123456789')

# Удаление клиента
delete_client(2)

# Поиск клиентов
print(find_client('Александр'))
