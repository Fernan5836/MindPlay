import random
import json
import os
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer
from juegos.juego_base import JuegoBase


class JuegoReconocimientoPatrones(JuegoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Juego de Reconocimiento de Patrones")
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Elementos de login y registro
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Usuario")
        self.layout.addWidget(self.nombre_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.registro_button = QPushButton("Registrarse")
        self.registro_button.clicked.connect(self.registro)
        self.layout.addWidget(self.registro_button)

        # Elementos del juego (inicialmente ocultos)
        self.usuario_label = QLabel()
        self.layout.addWidget(self.usuario_label)
        self.usuario_label.hide()

        self.nivel_label = QLabel()
        self.layout.addWidget(self.nivel_label)
        self.nivel_label.hide()

        self.secuencia_label = QLabel("Secuencia:")
        self.layout.addWidget(self.secuencia_label)
        self.secuencia_label.hide()

        self.respuesta_input = QLineEdit()
        self.layout.addWidget(self.respuesta_input)
        self.respuesta_input.hide()

        self.enviar_button = QPushButton("Enviar")
        self.enviar_button.clicked.connect(self.verificar_respuesta)
        self.layout.addWidget(self.enviar_button)
        self.enviar_button.hide()

        self.tiempo_label = QLabel("Tiempo: 60")
        self.layout.addWidget(self.tiempo_label)
        self.tiempo_label.hide()

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_tiempo)

        # Inicialización de variables
        self.tiempo_restante = 60
        self.secuencia_actual = []
        self.siguiente_numero = 0
        self.nivel = 1
        self.puntuacion = 0
        self.usuario_actual = None

        # Configuración de dificultad por nivel
        self.dificultad_por_nivel = {
            1: {"tiempo": 60, "min": 1, "max": 10, "diferencia": 2},
            2: {"tiempo": 50, "min": 5, "max": 15, "diferencia": 3},
            3: {"tiempo": 40, "min": 10, "max": 20, "diferencia": 4},
            4: {"tiempo": 30, "min": 15, "max": 25, "diferencia": 5},
            5: {"tiempo": 20, "min": 20, "max": 30, "diferencia": 6}
        }

        # Cargar usuarios si existe el archivo
        self.archivo_usuarios = 'usuarios.json'
        self.usuarios = self.cargar_usuarios()

    def cargar_usuarios(self):
        if os.path.exists(self.archivo_usuarios):
            with open(self.archivo_usuarios, 'r') as f:
                return json.load(f)
        return {}

    def guardar_usuarios(self):
        with open(self.archivo_usuarios, 'w') as f:
            json.dump(self.usuarios, f)

    def login(self):
        nombre = self.nombre_input.text()
        password = self.password_input.text()

        if nombre in self.usuarios and self.usuarios[nombre]['password'] == password:
            self.usuario_actual = nombre
            self.mostrar_interfaz_juego()
            self.iniciar_juego()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def registro(self):
        nombre = self.nombre_input.text()
        password = self.password_input.text()

        if nombre and password:
            if nombre not in self.usuarios:
                self.usuarios[nombre] = {
                    'password': password,
                    'max_nivel': 1,
                    'max_puntuacion': 0,
                    'total_partidas': 0
                }
                self.guardar_usuarios()
                QMessageBox.information(self, "Éxito", "Usuario registrado correctamente")
            else:
                QMessageBox.warning(self, "Error", "El usuario ya existe")
        else:
            QMessageBox.warning(self, "Error", "Complete todos los campos")

    def mostrar_interfaz_juego(self):
        # Ocultar elementos de login
        self.nombre_input.hide()
        self.password_input.hide()
        self.login_button.hide()
        self.registro_button.hide()

        # Mostrar elementos del juego
        self.usuario_label.show()
        self.nivel_label.show()
        self.secuencia_label.show()
        self.respuesta_input.show()
        self.enviar_button.show()
        self.tiempo_label.show()

    def iniciar_juego(self):
        self.puntuacion = 0
        self.nivel = 1
        self.actualizar_labels()
        self.tiempo_restante = self.dificultad_por_nivel[self.nivel]["tiempo"]
        self.generar_secuencia()
        self.timer.start(1000)

    def actualizar_labels(self):
        self.usuario_label.setText(f"Usuario: {self.usuario_actual}")
        self.nivel_label.setText(f"Nivel: {self.nivel}")

    def generar_secuencia(self):
        config = self.dificultad_por_nivel[self.nivel]
        tipo_secuencia = random.choice(["aritmetica", "geometrica", "fibonacci"])

        if tipo_secuencia == "aritmetica":
            inicio = random.randint(config["min"], config["max"])
            diferencia = random.randint(1, config["diferencia"])
            self.secuencia_actual = [inicio + i * diferencia for i in range(5)]
            self.siguiente_numero = self.secuencia_actual[-1] + diferencia

        elif tipo_secuencia == "geometrica":
            inicio = random.randint(config["min"], config["max"] // 2)
            razon = random.randint(2, config["diferencia"])
            self.secuencia_actual = [inicio * (razon ** i) for i in range(5)]
            self.siguiente_numero = self.secuencia_actual[-1] * razon

        else:  # Fibonacci
            a, b = config["min"], config["min"] + config["diferencia"]
            self.secuencia_actual = []
            for _ in range(5):
                self.secuencia_actual.append(a)
                a, b = b, a + b
            self.siguiente_numero = a

        self.secuencia_label.setText(
            f"Secuencia: {', '.join(map(str, self.secuencia_actual))}")
        self.respuesta_input.clear()
        self.respuesta_input.setFocus()

    def verificar_respuesta(self):
        respuesta_usuario = self.respuesta_input.text()
        if respuesta_usuario.isdigit() and int(respuesta_usuario) == self.siguiente_numero:
            self.puntuacion += self.nivel * 10
            if self.nivel < len(self.dificultad_por_nivel):
                self.nivel += 1
                self.tiempo_restante = self.dificultad_por_nivel[self.nivel]["tiempo"]
                QMessageBox.information(
                    self, "¡Correcto!",
                    f"¡Bien hecho! Pasas al nivel {self.nivel}\n"
                    f"Puntuación actual: {self.puntuacion}"
                )
            self.actualizar_labels()
        else:
            QMessageBox.warning(
                self, "Incorrecto",
                f"La respuesta correcta era {self.siguiente_numero}"
            )

        self.generar_secuencia()

    def actualizar_tiempo(self):
        self.tiempo_restante -= 1
        self.tiempo_label.setText(f"Tiempo: {self.tiempo_restante}")
        if self.tiempo_restante <= 0:
            self.timer.stop()
            self.finalizar_juego()

    def finalizar_juego(self):
        # Actualizar estadísticas del usuario
        if self.usuario_actual in self.usuarios:
            usuario = self.usuarios[self.usuario_actual]
            usuario['max_nivel'] = max(usuario['max_nivel'], self.nivel)
            usuario['max_puntuacion'] = max(usuario['max_puntuacion'], self.puntuacion)
            usuario['total_partidas'] += 1
            self.guardar_usuarios()

        mensaje = (
            f"¡Tiempo agotado!\n"
            f"Nivel alcanzado: {self.nivel}\n"
            f"Puntuación final: {self.puntuacion}\n\n"
            f"Récord personal: {usuario['max_puntuacion']}"
        )
        QMessageBox.information(self, "Fin del juego", mensaje)

        # Volver a la pantalla de login
        self.usuario_actual = None
        self.mostrar_interfaz_login()

    def mostrar_interfaz_login(self):
        # Mostrar elementos de login
        self.nombre_input.show()
        self.password_input.show()
        self.login_button.show()
        self.registro_button.show()

        # Ocultar elementos del juego
        self.usuario_label.hide()
        self.nivel_label.hide()
        self.secuencia_label.hide()
        self.respuesta_input.hide()
        self.enviar_button.hide()
        self.tiempo_label.hide()