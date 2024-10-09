from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from juegos.memoria import JuegoMemoria
from juegos.calculo_rapido import JuegoCalculoRapido
from juegos.reconocimiento_patrones import JuegoReconocimientoPatrones
from juegos.sudoku import JuegoSudoku
from functools import partial

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MindPlay")
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        juegos = [
            ("Memoria", JuegoMemoria),
            ("Cálculo Rápido", JuegoCalculoRapido),
            ("Reconocimiento de Patrones", JuegoReconocimientoPatrones),
            ("Sudoku", JuegoSudoku)
        ]

        for nombre, clase_juego in juegos:
            boton = QPushButton(nombre)
            boton.clicked.connect(partial(self.abrir_juego, clase_juego))
            layout.addWidget(boton)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def abrir_juego(self, clase_juego):
        if hasattr(self, 'juego_actual'):
            self.juego_actual.close()  # Cierra el juego anterior si existe
        self.juego_actual = clase_juego()
        self.juego_actual.show()
        # Comprueba si el método iniciar_juego existe antes de llamarlo
        if hasattr(self.juego_actual, 'iniciar_juego'):
            self.juego_actual.iniciar_juego()
