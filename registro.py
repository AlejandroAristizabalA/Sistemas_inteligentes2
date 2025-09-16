import json
from datetime import datetime

ARCHIVO = "registros.json"

def guardar_registro(nombre, edad, respuestas, resultado, consejo, score):
    """
    Guarda un registro de la evaluación en un archivo JSON.
    """
    nuevo_registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre": nombre,
        "edad": edad,
        "respuestas": respuestas,
        "resultado": resultado,
        "consejo": consejo,
        "score": score
    }

    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            registros = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        registros = []

    registros.append(nuevo_registro)

    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=4, ensure_ascii=False)

    return True

