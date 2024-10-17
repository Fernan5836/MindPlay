import random
from PyQt6.QtWidgets import (QVBoxLayout, QLabel, QLineEdit, QPushButton,
                             QMessageBox, QWidget, QHBoxLayout)
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QRect
from PyQt6.QtGui import QFont, QColor, QPalette
from juegos.juego_base import JuegoBase


class AnimatedLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def animate_success(self):
        self.setStyleSheet("""
            color: #4CAF50;
            font-weight: bold;
            font-size: 24px;
        """)
        QTimer.singleShot(500, self.reset_style)

    def animate_error(self):
        self.setStyleSheet("""
            color: #F44336;
            font-weight: bold;
            font-size: 24px;
        """)
        QTimer.singleShot(500, self.reset_style)

    def reset_style(self):
        self.setStyleSheet("""
            color: #1565C0;
            font-size: 22px;
        """)


class JuegoCalculoRapido(JuegoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧮 Cálculo Rápido")
        self.setGeometry(100, 100, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        # Configuración principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Estilo general
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
            }
            QLabel {
                color: #1565C0;
                font-size: 22px;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #2196F3;
                border-radius: 5px;
                font-size: 18px;
            }
        """)

        # Panel superior con estadísticas
        self.stats_layout = QHBoxLayout()

        # Tiempo
        self.tiempo_widget = QWidget()
        self.tiempo_widget.setStyleSheet("""
            QWidget {
                background-color: #E3F2FD;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.tiempo_layout = QVBoxLayout(self.tiempo_widget)
        self.tiempo_label = QLabel("⏱️ Tiempo")
        self.tiempo_valor = QLabel("30")
        self.tiempo_layout.addWidget(self.tiempo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.tiempo_layout.addWidget(self.tiempo_valor, alignment=Qt.AlignmentFlag.AlignCenter)

        # Puntuación
        self.puntos_widget = QWidget()
        self.puntos_widget.setStyleSheet("""
            QWidget {
                background-color: #E8F5E9;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.puntos_layout = QVBoxLayout(self.puntos_widget)
        self.puntos_label = QLabel("🎯 Puntos")
        self.puntos_valor = QLabel("0")
        self.puntos_layout.addWidget(self.puntos_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.puntos_layout.addWidget(self.puntos_valor, alignment=Qt.AlignmentFlag.AlignCenter)

        # Racha
        self.racha_widget = QWidget()
        self.racha_widget.setStyleSheet("""
            QWidget {
                background-color: #FFF3E0;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        self.racha_layout = QVBoxLayout(self.racha_widget)
        self.racha_label = QLabel("🔥 Racha")
        self.racha_valor = QLabel("0")
        self.racha_layout.addWidget(self.racha_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.racha_layout.addWidget(self.racha_valor, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stats_layout.addWidget(self.tiempo_widget)
        self.stats_layout.addWidget(self.puntos_widget)
        self.stats_layout.addWidget(self.racha_widget)

        self.layout.addLayout(self.stats_layout)

        # Pregunta
        self.pregunta_label = AnimatedLabel("¿Listo?")
        self.pregunta_label.setFont(QFont('Arial', 24))
        self.layout.addWidget(self.pregunta_label)

        # Campo de respuesta
        self.respuesta_container = QWidget()
        self.respuesta_layout = QHBoxLayout(self.respuesta_container)

        self.respuesta_input = QLineEdit()
        self.respuesta_input.setPlaceholderText("Escribe tu respuesta aquí")
        self.respuesta_input.returnPressed.connect(self.verificar_respuesta)

        self.enviar_button = QPushButton("Enviar")
        self.enviar_button.clicked.connect(self.verificar_respuesta)

        self.respuesta_layout.addWidget(self.respuesta_input)
        self.respuesta_layout.addWidget(self.enviar_button)

        self.layout.addWidget(self.respuesta_container)

        # Mensaje de retroalimentación
        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.feedback_label)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_tiempo)

        # Variables del juego
        self.tiempo_restante = 30
        self.respuesta_correcta = 0
        self.preguntas_respondidas = 0
        self.racha_actual = 0
        self.mejor_racha = 0
        self.dificultad = 1

    def iniciar_juego(self):
        self.puntuacion = 0
        self.preguntas_respondidas = 0
        self.racha_actual = 0
        self.mejor_racha = 0
        self.dificultad = 1
        self.tiempo_restante = 30
        self.actualizar_labels()
        self.generar_pregunta()
        self.timer.start(1000)
        self.respuesta_input.setFocus()

    def generar_pregunta(self):
        operaciones = {
            1: [('+', 1, 50), ('-', 1, 50), ('*', 1, 10)],
            2: [('+', 10, 100), ('-', 10, 100), ('*', 1, 12)],
            3: [('+', 50, 200), ('-', 50, 200), ('*', 10, 20)]
        }

        nivel = operaciones[self.dificultad]
        op, min_val, max_val = random.choice(nivel)

        if op == '+':
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            self.respuesta_correcta = a + b
        elif op == '-':
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, a)
            self.respuesta_correcta = a - b
        else:  # Multiplicación
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            self.respuesta_correcta = a * b

        self.pregunta_label.setText(f"{a} {op} {b} = ?")
        self.respuesta_input.clear()

    def verificar_respuesta(self):
        respuesta_usuario = self.respuesta_input.text()
        if not respuesta_usuario.strip():
            return

        try:
            respuesta = int(respuesta_usuario)
            if respuesta == self.respuesta_correcta:
                self.respuesta_correcta_accion()
            else:
                self.respuesta_incorrecta_accion()
        except ValueError:
            self.feedback_label.setText("¡Por favor, introduce un número válido!")
            self.feedback_label.setStyleSheet("color: #F44336;")

        self.preguntas_respondidas += 1
        self.respuesta_input.clear()
        self.generar_pregunta()

    def respuesta_correcta_accion(self):
        self.puntuacion += self.dificultad * 10
        self.racha_actual += 1
        self.mejor_racha = max(self.racha_actual, self.mejor_racha)

        # Aumentar dificultad cada 5 respuestas correctas
        if self.racha_actual % 5 == 0 and self.dificultad < 3:
            self.dificultad += 1
            self.tiempo_restante += 10  # Bonus de tiempo
            self.feedback_label.setText("¡Nivel aumentado! +10 segundos")
        else:
            self.feedback_label.setText("¡Correcto! 🎉")

        self.pregunta_label.animate_success()
        self.feedback_label.setStyleSheet("color: #4CAF50;")
        self.actualizar_labels()

    def respuesta_incorrecta_accion(self):
        self.racha_actual = 0
        self.pregunta_label.animate_error()
        self.feedback_label.setText(f"¡Incorrecto! La respuesta era {self.respuesta_correcta}")
        self.feedback_label.setStyleSheet("color: #F44336;")
        self.actualizar_labels()

    def actualizar_tiempo(self):
        self.tiempo_restante -= 1
        self.tiempo_valor.setText(str(self.tiempo_restante))

        if self.tiempo_restante <= 5:
            self.tiempo_valor.setStyleSheet("color: #F44336; font-weight: bold;")

        if self.tiempo_restante <= 0:
            self.timer.stop()
            self.finalizar_juego()

    def actualizar_labels(self):
        self.puntos_valor.setText(str(self.puntuacion))
        self.racha_valor.setText(str(self.racha_actual))
        self.tiempo_valor.setText(str(self.tiempo_restante))

    def finalizar_juego(self):
        precision = (self.puntuacion // (self.dificultad * 10)) / max(1, self.preguntas_respondidas) * 100

        mensaje = (
            f"🎮 ¡Juego terminado!\n\n"
            f"📊 Estadísticas:\n"
            f"✨ Puntuación final: {self.puntuacion}\n"
            f"📝 Preguntas respondidas: {self.preguntas_respondidas}\n"
            f"🎯 Precisión: {precision:.1f}%\n"
            f"🔥 Mejor racha: {self.mejor_racha}\n"
            f"📈 Nivel máximo alcanzado: {self.dificultad}\n"
        )

        QMessageBox.information(self, "🏆 Fin del juego", mensaje)
        self.close()