import random
import matplotlib.pyplot as plt
import numpy as np
import io
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QDialog

# --- Texto del informe basado en reglas ---
def generar_informe_offline(respuestas: dict, edad: int) -> str:
    sintomas_graves = ["Dolor en el pecho", "Dificultad para respirar", "Fiebre"]
    sintomas_moderados = ["Dolor de cabeza", "Cansancio", "Problemas de sueño"]
    
    graves = [s for s in respuestas.values() if s in sintomas_graves]
    moderados = [s for s in respuestas.values() if s in sintomas_moderados]

    if graves:
        urgencia = "ALTA"
        resumen = "Presentas síntomas que requieren atención médica inmediata."
    elif len(moderados) >= 2:
        urgencia = "MEDIA"
        resumen = "Presentas malestares moderados, es recomendable observar y consultar al médico si persisten."
    else:
        urgencia = "BAJA"
        resumen = "Tus síntomas son leves, mantén cuidados generales."

    # Bloque de datos aleatorios
    severidad = random.randint(10, 90)
    energia = random.choice(["Alta", "Moderada", "Baja"])
    consejos = [
        "Bebe suficiente agua hoy.",
        "Realiza estiramientos suaves.",
        "Tómate un descanso de 15 minutos en la tarde.",
        "Escucha música relajante.",
        "Camina 10 minutos si te sientes con energía."
    ]
    consejo = random.choice(consejos)

    informe = (
        f"📋 Resumen: {resumen}\n"
        f"⚠️ Nivel de urgencia: {urgencia}\n"
        f"📊 Severidad estimada: {severidad}%\n"
        f"🔋 Energía recomendada: {energia}\n"
        f"💡 Consejo del día: {consejo}\n"
        f"\nNota: Esto es orientación, no un diagnóstico médico."
    )
    return informe

# --- Gráfica de riesgo por edad ---
def generar_grafica_riesgo(edad_usuario: int) -> QPixmap:
    edades = np.arange(40, 91, 5)
    riesgos = []

    for e in edades:
        distancia = abs(e - edad_usuario)
        base = max(20, 100 - distancia*4)
        riesgo = base + random.randint(-10, 10)
        riesgos.append(min(100, max(10, riesgo)))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(edades, riesgos, width=4, color="#4C72B0")
    ax.set_title("Riesgo relativo según la edad", fontsize=12, fontweight="bold")
    ax.set_xlabel("Edad")
    ax.set_ylabel("Nivel de riesgo (%)")
    ax.axvline(edad_usuario, color="red", linestyle="--", label=f"Tu edad: {edad_usuario}")
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    pixmap = QPixmap()
    pixmap.loadFromData(buf.getvalue())
    plt.close(fig)

    return pixmap

# --- Ventana combinada ---
class InformeDialog(QDialog):
    def __init__(self, informe_texto: str, edad: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informe completo")
        self.resize(800, 600)

        layout = QVBoxLayout()

        label_texto = QLabel(informe_texto)
        label_texto.setWordWrap(True)
        layout.addWidget(label_texto)

        pixmap = generar_grafica_riesgo(edad)
        label_grafica = QLabel()
        label_grafica.setPixmap(pixmap)
        layout.addWidget(label_grafica)

        self.setLayout(layout)
