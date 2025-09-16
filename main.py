import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

def main():
    app = QApplication(sys.argv)

    ventana = QWidget()
    ventana.setWindowTitle("Asistente de Salud")
    ventana.resize(400, 200)

    layout = QVBoxLayout()
    label = QLabel("¡Hola! Bienvenido al Asistente de Salud 🩺")
    layout.addWidget(label)

    ventana.setLayout(layout)
    ventana.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
