from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase

USER = "postgres"
HOST = "localhost"
PASSWORD = "poltava1955"

create_database = f'CREATE DATABASE server_db;'
create_table_users = f'''CREATE TABLE users(
    id serial PRIMARY KEY, 
    username varchar(255) UNIQUE NOT NULL, 
    hashed_password varchar(80) NOT NULL);'''
create_table_messages = f'''CREATE TABLE messages(
    id serial PRIMARY KEY, 
    from_id int NOT NULL REFERENCES users(id) ON DELETE CASCADE, 
    to_id int NOT NULL REFERENCES users(id) ON DELETE CASCADE, 
    text varchar(255), 
    creation_date timestamp DEFAULT CURRENT_TIMESTAMP);'''

try:
    with connect(user=USER, password=PASSWORD, host=HOST) as connection:
        with connection.cursor() as cursor:
            connection.autocommit = True
            try:
                cursor.execute(create_database)
                print("Database is created.")
            except DuplicateDatabase as ex:
                print('Database is already exist.', ex)
except OperationalError as ex:
    print('Connection error. Check all data and try again.', ex)

try:
    with connect(user=USER, password=PASSWORD, host=HOST, database='server_db') as connection:
        with connection.cursor() as cursor:
            connection.autocommit = True
            try:
                cursor.execute(create_table_users)
                print("Table is created.")
            except DuplicateDatabase as ex:
                print('Table is already exist.', ex)
            try:
                cursor.execute(create_table_messages)
                print("Table is created.")
            except DuplicateDatabase as ex:
                print('Table is already exist.', ex)
except OperationalError as ex:
    print('Connection error. Check all data and try again.', ex)
