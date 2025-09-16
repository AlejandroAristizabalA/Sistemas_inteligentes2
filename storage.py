import json
import os

FILE_NAME = "usuarios.json"

def cargar_usuarios():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_usuario(nombre, edad, genero, contacto):
    usuarios = cargar_usuarios()
    usuarios.append({
        "nombre": nombre,
        "edad": edad,
        "genero": genero,
        "contacto": contacto
    })
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
