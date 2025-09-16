import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QListWidget
)
from storage import guardar_usuario, cargar_usuarios

class FormularioRegistro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario — Asistente de Salud")
        self.resize(400, 400)

        layout = QVBoxLayout()

        # Campos
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")

        self.edad_input = QLineEdit()
        self.edad_input.setPlaceholderText("Edad")

        self.genero_input = QComboBox()
        self.genero_input.addItems(["Seleccionar", "Masculino", "Femenino", "Otro"])

        self.contacto_input = QLineEdit()
        self.contacto_input.setPlaceholderText("Número de contacto")

        # Botón guardar
        self.boton_guardar = QPushButton("Guardar Usuario")
        self.boton_guardar.clicked.connect(self.guardar_usuario)

        # Lista para mostrar usuarios
        self.lista_usuarios = QListWidget()
        self.cargar_usuarios()

        # Agregar al layout
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_input)

        layout.addWidget(QLabel("Edad:"))
        layout.addWidget(self.edad_input)

        layout.addWidget(QLabel("Género:"))
        layout.addWidget(self.genero_input)

        layout.addWidget(QLabel("Contacto:"))
        layout.addWidget(self.contacto_input)

        layout.addWidget(self.boton_guardar)
        layout.addWidget(QLabel("Usuarios registrados:"))
        layout.addWidget(self.lista_usuarios)

        self.setLayout(layout)

    def guardar_usuario(self):
        nombre = self.nombre_input.text().strip()
        edad = self.edad_input.text().strip()
        genero = self.genero_input.currentText()
        contacto = self.contacto_input.text().strip()

        if not nombre or not edad.isdigit() or genero == "Seleccionar" or not contacto:
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos correctamente.")
            return

        guardar_usuario(nombre, int(edad), genero, contacto)
        QMessageBox.information(self, "Éxito", f"Usuario {nombre} guardado correctamente.")

        # Limpiar campos
        self.nombre_input.clear()
        self.edad_input.clear()
        self.contacto_input.clear()
        self.genero_input.setCurrentIndex(0)

        # Recargar lista
        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.lista_usuarios.clear()
        usuarios = cargar_usuarios()
        for u in usuarios:
            self.lista_usuarios.addItem(f"{u['nombre']} ({u['edad']} años) - {u['genero']} - {u['contacto']}")
from diagnostico import generar_informe_offline, InformeDialog

def on_evaluar_clicked(self):
    respuestas = {preg: combo.currentText() for preg, combo in self.respuestas.items()}
    edad = 70  # Ejemplo: luego puedes cargarla del perfil

    informe = generar_informe_offline(respuestas, edad)

    dlg = InformeDialog(informe, edad, parent=self)
    dlg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FormularioRegistro()
    ventana.show()
    sys.exit(app.exec())
