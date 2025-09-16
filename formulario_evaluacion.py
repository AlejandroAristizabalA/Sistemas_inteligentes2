import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLineEdit, QMessageBox, QFrame, QTextEdit
)
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt
from registro import guardar_registro


# -------- Generador de gráfica de riesgo --------
def generar_pixmap_riesgo(edad_usuario: int, score: int, estado: str, width=500, height=250):
    """
    Genera una gráfica lógica y minimalista:
    - Riesgo base crece con la edad.
    - Riesgo adicional depende del score.
    - El color de la barra del usuario cambia según gravedad.
    """
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.white)
    painter = QPainter(pixmap)

    # Colores según estado
    colores_estado = {
        "ok": QColor(80, 180, 80),       # verde
        "leve": QColor(230, 200, 40),    # amarillo
        "grave": QColor(200, 60, 60)     # rojo
    }

    # Grupos de edad en décadas
    age_groups = list(range(20, 91, 10))
    riesgos = []

    for edad in age_groups:
        riesgo_base = edad / 10
        riesgo_sintomas = score * 0.8
        riesgo_total = min(10, int(riesgo_base + riesgo_sintomas))
        riesgos.append(riesgo_total)

    max_riesgo = max(riesgos) if riesgos else 1
    bar_width = width // len(age_groups)

    for i, edad in enumerate(age_groups):
        bar_height = int((riesgos[i] / max_riesgo) * (height - 40))
        x = i * bar_width
        y = height - bar_height

        # Si coincide con edad usuario, aplicar color dinámico
        if edad <= edad_usuario < edad + 10:
            if estado == "ok":
                painter.setBrush(colores_estado["ok"])
            elif estado == "leve":
                painter.setBrush(colores_estado["leve"])
            else:
                painter.setBrush(colores_estado["grave"])
        else:
            painter.setBrush(QColor(220, 220, 220))  # gris claro

        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawRect(x + 8, y, bar_width - 16, bar_height)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(x + 12, height - 5, str(edad))

    painter.end()
    return pixmap


# -------- Ventana principal --------
class FormularioEvaluacion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chequeo Diario de Salud")
        self.resize(700, 600)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        # Título
        titulo = QLabel("🩺 Chequeo Diario de Salud")
        titulo.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitulo = QLabel("Complete las preguntas para recibir un diagnóstico visual y consejo personalizado")
        subtitulo.setFont(QFont("Segoe UI", 12))
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitulo.setStyleSheet("color: gray;")

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # Preguntas
        self.preguntas = [
            "¿Tiene fiebre hoy?",
            "¿Siente dolor de cabeza?",
            "¿Tiene tos?",
            "¿Le duele el pecho?",
            "¿Tiene dificultad para respirar?",
            "¿Cómo califica su nivel de energía?",
            "¿Ha tenido mareos?",
            "¿Tiene dolor muscular?",
            "¿Su apetito fue normal?",
            "¿Ha dormido bien?"
        ]

        self.combos = []
        preguntas_layout = QVBoxLayout()

        # Campo edad
        edad_layout = QHBoxLayout()
        lbl_edad = QLabel("Edad:")
        lbl_edad.setFont(QFont("Segoe UI", 12))
        self.edad_input = QLineEdit()
        self.edad_input.setPlaceholderText("Ingrese su edad")
        self.edad_input.setFixedWidth(100)
        edad_layout.addWidget(lbl_edad)
        edad_layout.addWidget(self.edad_input)
        preguntas_layout.addLayout(edad_layout)

        opciones = ["Sí", "No", "Leve"]

        for preg in self.preguntas:
            row = QHBoxLayout()
            lbl = QLabel(preg)
            lbl.setFont(QFont("Segoe UI", 11))
            combo = QComboBox()
            combo.addItems(opciones)
            combo.setFixedWidth(100)
            self.combos.append(combo)
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(combo)
            preguntas_layout.addLayout(row)

        layout.addLayout(preguntas_layout)

        # Botón
        self.btn_evaluar = QPushButton("Evaluar mi estado")
        self.btn_evaluar.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.btn_evaluar.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.btn_evaluar.clicked.connect(self.evaluar)
        layout.addWidget(self.btn_evaluar, alignment=Qt.AlignmentFlag.AlignCenter)

    def evaluar(self):
        try:
            edad_text = self.edad_input.text()
            edad = int(edad_text) if edad_text else 70
            if edad < 1 or edad > 130:
                QMessageBox.warning(self, "Edad fuera de rango", "Se recomienda entre 1 y 130 años. Ajusta si fue un error.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese una edad válida.")
            return

        respuestas = [c.currentText() for c in self.combos]
        score = respuestas.count("Sí") * 2 + respuestas.count("Leve")

        if score == 0:
            estado = "ok"
            titulo = "Todo parece estar bien."
            consejo = "Mantenga hábitos saludables y siga cuidando su salud."
        elif score <= 4:
            estado = "leve"
            titulo = "Síntomas leves."
            consejo = "Descanse y monitoree los síntomas."
        else:
            estado = "grave"
            titulo = "Alerta: considere consultar un médico."
            consejo = "Busque atención médica lo antes posible."

        # Guardar
        respuestas_dict = dict(zip(self.preguntas, respuestas))
        guardar_registro(
            nombre="Paciente",
            edad=edad,
            respuestas=respuestas_dict,
            resultado=titulo,
            consejo=consejo,
            score=score
        )

        # Resultado
        ventana = QWidget()
        ventana.setWindowTitle("Resultado de la Evaluación")
        layout = QVBoxLayout(ventana)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 20, 40, 20)

        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setFont(QFont("Segoe UI", 13))
        txt.setStyleSheet("background: #f9f9f9; border-radius: 10px; padding: 10px;")
        txt.setText(
            f"👤 Edad: {edad}\n"
            f"📊 Severidad estimada: {score}/20\n"
            f"⚠️ Estado: {titulo}\n"
            f"💡 Consejo: {consejo}"
        )

        lbl_grafica = QLabel()
        lbl_grafica.setPixmap(generar_pixmap_riesgo(edad, score, estado, 600, 250))
        lbl_grafica.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(txt)
        layout.addWidget(lbl_grafica)

        ventana.resize(650, 600)
        ventana.show()
        ventana.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.resultado = ventana


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FormularioEvaluacion()
    ventana.show()
    sys.exit(app.exec())
