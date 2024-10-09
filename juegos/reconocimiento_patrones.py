import random
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

        self.secuencia_label = QLabel("Secuencia:")
        self.layout.addWidget(self.secuencia_label)

        self.respuesta_input = QLineEdit()
        self.layout.addWidget(self.respuesta_input)

        self.enviar_button = QPushButton("Enviar")
        self.enviar_button.clicked.connect(self.verificar_respuesta)
        self.layout.addWidget(self.enviar_button)

        self.tiempo_label = QLabel("Tiempo: 60")
        self.layout.addWidget(self.tiempo_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_tiempo)

        self.tiempo_restante = 60
        self.secuencia_actual = []
        self.siguiente_numero = 0
        self.nivel = 1

    def iniciar_juego(self):
        self.puntuacion = 0
        self.nivel = 1
        self.tiempo_restante = 60
        self.generar_secuencia()
        self.timer.start(1000)  # Actualizar cada segundo

    def generar_secuencia(self):
        tipo_secuencia = random.choice(["aritmetica", "geometrica", "fibonacci"])

        if tipo_secuencia == "aritmetica":
            inicio = random.randint(1, 10)
            diferencia = random.randint(1, 5)
            self.secuencia_actual = [inicio + i * diferencia for i in range(5)]
            self.siguiente_numero = self.secuencia_actual[-1] + diferencia

        elif tipo_secuencia == "geometrica":
            inicio = random.randint(1, 5)
            razon = random.randint(2, 3)
            self.secuencia_actual = [inicio * (razon ** i) for i in range(5)]
            self.siguiente_numero = self.secuencia_actual[-1] * razon

        else:  # Fibonacci
            a, b = 0, 1
            self.secuencia_actual = []
            for _ in range(5):
                self.secuencia_actual.append(a)
                a, b = b, a + b
            self.siguiente_numero = a

        self.secuencia_label.setText(f"Secuencia: {', '.join(map(str, self.secuencia_actual))}")
        self.respuesta_input.clear()
        self.respuesta_input.setFocus()

    def verificar_respuesta(self):
        respuesta_usuario = self.respuesta_input.text()
        if respuesta_usuario.isdigit() and int(respuesta_usuario) == self.siguiente_numero:
            self.puntuacion += self.nivel
            self.nivel += 1
            QMessageBox.information(self, "¡Correcto!", f"¡Bien hecho! Pasas al nivel {self.nivel}")
        else:
            QMessageBox.warning(self, "Incorrecto", f"La respuesta correcta era {self.siguiente_numero}")

        self.generar_secuencia()

    def actualizar_tiempo(self):
        self.tiempo_restante -= 1
        self.tiempo_label.setText(f"Tiempo: {self.tiempo_restante}")
        if self.tiempo_restante <= 0:
            self.timer.stop()
            self.finalizar_juego()

    def finalizar_juego(self):
        mensaje = (f"¡Tiempo agotado!\n"
                   f"Nivel alcanzado: {self.nivel}\n"
                   f"Puntuación final: {self.puntuacion}")
        QMessageBox.information(self, "Fin del juego", mensaje)
        self.close()