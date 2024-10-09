import random
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer
from juegos.juego_base import JuegoBase

class JuegoCalculoRapido(JuegoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Juego de Cálculo Rápido")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.pregunta_label = QLabel("Preparado?")
        self.layout.addWidget(self.pregunta_label)

        self.respuesta_input = QLineEdit()
        self.layout.addWidget(self.respuesta_input)

        self.enviar_button = QPushButton("Enviar")
        self.enviar_button.clicked.connect(self.verificar_respuesta)
        self.layout.addWidget(self.enviar_button)

        self.tiempo_label = QLabel("Tiempo: 30")
        self.layout.addWidget(self.tiempo_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_tiempo)

        self.tiempo_restante = 30
        self.respuesta_correcta = 0
        self.preguntas_respondidas = 0

    def iniciar_juego(self):
        self.puntuacion = 0
        self.preguntas_respondidas = 0
        self.generar_pregunta()
        self.tiempo_restante = 30
        self.timer.start(1000)  # Actualizar cada segundo

    def generar_pregunta(self):
        operacion = random.choice(['+', '-', '*'])
        if operacion == '+':
            a = random.randint(1, 50)
            b = random.randint(1, 50)
            self.respuesta_correcta = a + b
        elif operacion == '-':
            a = random.randint(1, 50)
            b = random.randint(1, a)  # Aseguramos que b <= a para evitar números negativos
            self.respuesta_correcta = a - b
        else:  # Multiplicación
            a = random.randint(1, 12)
            b = random.randint(1, 12)
            self.respuesta_correcta = a * b

        self.pregunta_label.setText(f"{a} {operacion} {b} = ?")
        self.respuesta_input.clear()
        self.respuesta_input.setFocus()

    def verificar_respuesta(self):
        respuesta_usuario = self.respuesta_input.text()
        if respuesta_usuario.isdigit() and int(respuesta_usuario) == self.respuesta_correcta:
            self.puntuacion += 1
        self.preguntas_respondidas += 1
        self.generar_pregunta()

    def actualizar_tiempo(self):
        self.tiempo_restante -= 1
        self.tiempo_label.setText(f"Tiempo: {self.tiempo_restante}")
        if self.tiempo_restante <= 0:
            self.timer.stop()
            self.finalizar_juego()

    def finalizar_juego(self):
        mensaje = (f"¡Tiempo agotado!\n"
                   f"Preguntas respondidas: {self.preguntas_respondidas}\n"
                   f"Respuestas correctas: {self.puntuacion}\n"
                   f"Puntuación final: {self.puntuacion}")
        QMessageBox.information(self, "Fin del juego", mensaje)
        self.close()