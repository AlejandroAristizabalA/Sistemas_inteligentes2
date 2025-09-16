import json
import os
from datetime import datetime

FILE_NAME = "evaluaciones.json"

def cargar_evaluaciones():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_evaluacion(usuario, respuestas, resultado):
    evaluaciones = cargar_evaluaciones()
    evaluaciones.append({
        "usuario": usuario,
        "respuestas": respuestas,
        "resultado": resultado,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(evaluaciones, f, indent=4, ensure_ascii=False)
