import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget,
    QDialog, QHBoxLayout, QListWidgetItem
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from formulario_evaluacion import FormularioEvaluacion


ARCHIVO = "registros.json"


class HistorialDialog(QDialog):
    """Ventana emergente para mostrar historial de evaluaciones"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Historial de Evaluaciones")
        self.resize(600, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("📜 Historial de evaluaciones")
        titulo.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        self.lista = QListWidget()
        self.lista.setStyleSheet("""
            QListWidget {
                background: #fafafa;
                border: none;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 10px;
            }
        """)
        layout.addWidget(self.lista)

        self.cargar_registros()

    def cargar_registros(self):
        try:
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                registros = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            registros = []

        if not registros:
            self.lista.addItem("⚠️ No hay registros disponibles.")
            return

        for reg in registros[::-1]:  # mostrar más recientes primero
            estado = reg["resultado"]
            color = "#4CAF50"  # verde por defecto
            if "leve" in estado.lower():
                color = "#e6c828"  # amarillo
            elif "alerta" in estado.lower():
                color = "#d9534f"  # rojo

            item = QListWidgetItem(
                f"{reg['fecha']} | Edad: {reg['edad']} | {estado}"
            )
            item.setForeground(QColor(color))
            self.lista.addItem(item)


class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.resize(500, 400)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(60, 40, 60, 40)

        titulo = QLabel("🏥 Sistema de Chequeo de Salud")
        titulo.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitulo = QLabel("Seleccione una opción para continuar")
        subtitulo.setFont(QFont("Segoe UI", 12))
        subtitulo.setStyleSheet("color: gray;")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(titulo)
        layout.addWidget(subtitulo)

        # Botones
        btn_evaluacion = QPushButton("🩺 Chequeo diario de salud")
        btn_evaluacion.clicked.connect(self.abrir_evaluacion)

        btn_historial = QPushButton("📜 Ver historial de evaluaciones")
        btn_historial.clicked.connect(self.ver_historial)

        btn_salir = QPushButton("🚪 Salir")
        btn_salir.clicked.connect(self.close)

        for btn in [btn_evaluacion, btn_historial, btn_salir]:
            btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333;
                    color: white;
                    padding: 12px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
            """)
            layout.addWidget(btn)

        layout.addStretch()

    def abrir_evaluacion(self):
        self.ventana_evaluacion = FormularioEvaluacion()
        self.ventana_evaluacion.show()

    def ver_historial(self):
        dlg = HistorialDialog()
        dlg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MenuPrincipal()
    ventana.show()
    sys.exit(app.exec())
