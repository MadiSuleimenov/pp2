# import psycopg2
# conn = psycopg2.connect(
#     host="localhost",
#     user="postgres",
#     password="1234",
#     dbname="phonebook"
# )
# print("Connected!")
# conn.close()


import psycopg2
from config import DB_CONFIG
def get_connection():
    return psycopg2.connect(**DB_CONFIG)

import psycopg2
def get_connection():
    return psycopg2.connect(
        host="localhost",      
        database="phonebook",   
        user="postgres",        
        password="1234"
    )
