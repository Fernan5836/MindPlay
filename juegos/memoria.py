import random
from PyQt6.QtWidgets import QGridLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer
from juegos.juego_base import JuegoBase


class CartaBoton(QPushButton):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor
        self.setText("?")
        self.setStyleSheet("font-size: 20px; min-width: 50px; min-height: 50px;")


class JuegoMemoria(JuegoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Juego de Memoria")
        self.setGeometry(100, 100, 400, 400)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.cartas = []
        self.carta_volteada = None
        self.puede_voltear = True
        self.pares_encontrados = 0

    def iniciar_juego(self):
        self.puntuacion = 0
        self.pares_encontrados = 0
        self.crear_tablero()

    def crear_tablero(self):
        valores = list(range(1, 9)) * 2
        random.shuffle(valores)

        for i in range(4):
            for j in range(4):
                carta = CartaBoton(valores.pop())
                carta.clicked.connect(lambda checked, c=carta: self.voltear_carta(c))
                self.layout.addWidget(carta, i, j)
                self.cartas.append(carta)

    def voltear_carta(self, carta):
        if not self.puede_voltear or carta.text() != "?":
            return

        carta.setText(str(carta.valor))

        if self.carta_volteada is None:
            self.carta_volteada = carta
        else:
            self.puede_voltear = False
            if self.carta_volteada.valor == carta.valor:
                self.pares_encontrados += 1
                self.puntuacion += 10
                self.carta_volteada = None
                self.puede_voltear = True
                if self.pares_encontrados == 8:
                    self.finalizar_juego()
            else:
                QTimer.singleShot(1000, lambda: self.ocultar_cartas(self.carta_volteada, carta))

    def ocultar_cartas(self, carta1, carta2):
        carta1.setText("?")
        carta2.setText("?")
        self.carta_volteada = None
        self.puede_voltear = True

    def finalizar_juego(self):
        mensaje = f"¡Felicidades! Has completado el juego.\nPuntuación final: {self.puntuacion}"
        QMessageBox.information(self, "Fin del juego", mensaje)
        self.close()