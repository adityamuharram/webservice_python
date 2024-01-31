import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="rest_db",
        user='postgres',
        password='1234')
