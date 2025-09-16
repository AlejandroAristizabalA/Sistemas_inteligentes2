import sqlite3

DB_NAME = "asistente_salud.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def crear_usuario(nombre, edad, genero, contacto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, edad, genero, contacto) VALUES (?, ?, ?, ?)",
        (nombre, edad, genero, contacto)
    )
    conn.commit()
    conn.close()

def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios
