import os
import hashlib
from datetime import datetime, date
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def consultar(sql, datos=()):
    con = conectar()
    cur = con.cursor()
    cur.execute(sql, datos)
    filas = cur.fetchall()
    con.close()
    return filas


def hash_clave(texto):
    return hashlib.sha256(texto.encode()).hexdigest()


def fecha(texto):
    try:
        return datetime.strptime(texto.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise Exception("Fecha inválida. Use dd/mm/aaaa")


def mostrar(fila):
    return [x.strftime("%d/%m/%Y") if isinstance(x, date) else x for x in fila]