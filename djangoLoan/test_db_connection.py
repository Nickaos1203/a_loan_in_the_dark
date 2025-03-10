# test_db_connection.py
import os
import pyodbc

server = 'lgallussqlserver.database.windows.net'
database = 'bddussba'
username = 'leo'
password = 'leflibustierdu59!'
driver = 'ODBC Driver 18 for SQL Server'

connection_string = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;"

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    print("Connexion réussie à la base de données Azure SQL!")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Erreur de connexion: {e}")