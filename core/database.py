# core/database.py
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Retorna uma conexão padrão baseada no arquivo .env"""
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    
    if user and password:
        # Autenticação SQL
        conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
    else:
        # Autenticação Windows
        conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
        
    return pyodbc.connect(conn_str)
