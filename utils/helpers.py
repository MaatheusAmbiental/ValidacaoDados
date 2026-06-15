# utils/helpers.py
import datetime
import os

def log_error(error_msg):
    """Salva erros em um arquivo local 'error_log.txt' para depuração"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a") as f:
        f.write(f"[{timestamp}] ERROR: {error_msg}\n")

def check_file_extension(filename, allowed=['xlsx', 'xls', 'csv']):
    """Valida extensões de arquivos (caso utilize importação manual de arquivos futuramente)"""
    ext = filename.split('.')[-1].lower()
    return ext in allowed

def format_sql_date(date_obj):
    """Garante que a data esteja no formato ISO para queries SQL"""
    if isinstance(date_obj, datetime.datetime):
        return date_obj.strftime("%Y-%m-%d")
    return date_obj
