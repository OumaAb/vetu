# db.py - Shared database connection helper
# All microservices import this file

import mysql.connector

DB_CONFIG = {
    "host": "mysql",
    "user": "rental_user",
    "password": "rental123",   
    "database": "clothes_rental",
    "port": 3306         
}

def get_connection():
    """Returns a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)
