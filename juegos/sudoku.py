import random
from PyQt6.QtWidgets import QGridLayout, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from juegos.juego_base import JuegoBase


class GeneradorPuzzle(QThread):
    puzzle_generado = pyqtSignal(list)

    def __init__(self, dificultad):
        super().__init__()
        self.dificultad = dificultad

    def run(self):
        puzzle = self.generar_puzzle_valido()
        self.puzzle_generado.emit(puzzle)

    def generar_puzzle_valido(self):
        base = 3
        side = base * base

        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle(s):
            return random.sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = int(squares * self.dificultad)
        for p in random.sample(range(squares), empties):
            board[p // side][p % side] = 0

        return board


class CeldaSudoku(QPushButton):
    def __init__(self, fila, columna):
        super().__init__()
        self.fila = fila
        self.columna = columna
        self.valor = 0
        self.fijo = False
        self.setFixedSize(50, 50)
        self.setFont(QFont('Arial', 16))
        self.actualizar_estilo()

    def actualizar_estilo(self):
        region = (self.fila // 3) * 3 + (self.columna // 3)
        color_base = QColor.fromHsv(region * 30, 100, 240)
        color_hover = color_base.lighter(110)

        estilo = f"""
        QPushButton {{
            background-color: {color_base.name()};
            border: 1px solid #00FFFF;
            color: yellow;  // Texto negro para mejor contraste
        }}
        QPushButton:hover {{
            background-color: {color_hover.name()};
        }}
        QPushButton:disabled {{
            color: #e74c3c;
            font-weight: bold;
        }}
        """

        # Agregar bordes más gruesos para separar regiones 3x3
        if self.fila % 3 == 0 and self.fila != 0:
            estilo += "border-top: 10px solid black;"
        if self.columna % 3 == 0 and self.columna != 0:
            estilo += "border-left: 10px solid black;"

        self.setStyleSheet(estilo)

    def set_valor(self, valor):
        self.valor = valor
        self.setText(str(valor) if valor != 0 else "")

    def set_fijo(self, fijo):
        self.fijo = fijo
        self.setEnabled(not fijo)
        font = self.font()
        font.setBold(fijo)
        self.setFont(font)

class JuegoSudoku(JuegoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setGeometry(100, 100, 500, 650)

        layout_principal = QVBoxLayout()
        self.setLayout(layout_principal)

        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        layout_principal.addLayout(self.grid)

        self.celdas = [[None for _ in range(9)] for _ in range(9)]
        self.crear_tablero()

        controles_layout = QHBoxLayout()
        self.dificultad_combo = QComboBox()
        self.dificultad_combo.addItems(["Fácil", "Medio", "Difícil"])
        controles_layout.addWidget(self.dificultad_combo)

        self.nuevo_juego_btn = QPushButton("Nuevo Juego")
        self.nuevo_juego_btn.clicked.connect(self.iniciar_juego)
        controles_layout.addWidget(self.nuevo_juego_btn)

        self.verificar_btn = QPushButton("Verificar")
        self.verificar_btn.clicked.connect(self.verificar_solucion)
        controles_layout.addWidget(self.verificar_btn)

        layout_principal.addLayout(controles_layout)

        self.mensaje_label = QLabel("")
        self.mensaje_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(self.mensaje_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_tiempo)
        self.tiempo = 0
        self.tiempo_label = QLabel("Tiempo: 00:00")
        layout_principal.addWidget(self.tiempo_label)

    def crear_tablero(self):
        for i in range(9):
            for j in range(9):
                celda = CeldaSudoku(i, j)
                celda.clicked.connect(self.celda_clickeada)
                self.grid.addWidget(celda, i, j)
                self.celdas[i][j] = celda

                # Añadir bordes más gruesos para separar las regiones 3x3
                if i % 3 == 0 and i != 0:
                    celda.setStyleSheet(celda.styleSheet() + "border-top: 10px solid black;")
                if j % 3 == 0 and j != 0:
                    celda.setStyleSheet(celda.styleSheet() + "border-left: 10px solid black;")

    def iniciar_juego(self):
        dificultad = self.dificultad_combo.currentText()
        dificultad_valor = {"Fácil": 0.3, "Medio": 0.5, "Difícil": 0.7}[dificultad]
        self.generador = GeneradorPuzzle(dificultad_valor)
        self.generador.puzzle_generado.connect(self.aplicar_puzzle)
        self.generador.start()
        self.tiempo = 0
        self.timer.start(1000)
        self.mensaje_label.setText("Generando puzzle...")
        self.nuevo_juego_btn.setEnabled(False)

    def aplicar_puzzle(self, puzzle):
        for i in range(9):
            for j in range(9):
                self.celdas[i][j].set_valor(puzzle[i][j])
                self.celdas[i][j].set_fijo(puzzle[i][j] != 0)
        self.mensaje_label.setText("¡Nuevo juego iniciado!")
        self.nuevo_juego_btn.setEnabled(True)

    def celda_clickeada(self):
        celda = self.sender()
        if not celda.fijo:
            nuevo_valor = celda.valor % 9 + 1
            celda.set_valor(nuevo_valor)

    def verificar_solucion(self):
        if self.es_solucion_valida():
            self.mensaje_label.setText("¡Felicidades! Has resuelto el Sudoku.")
            self.timer.stop()
        else:
            self.mensaje_label.setText("La solución no es correcta. Sigue intentando.")

    def es_solucion_valida(self):
        # Verificar filas y columnas
        for i in range(9):
            if not self.es_secuencia_valida([self.celdas[i][j].valor for j in range(9)]) or \
                    not self.es_secuencia_valida([self.celdas[j][i].valor for j in range(9)]):
                return False

        # Verificar regiones 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if not self.es_secuencia_valida([self.celdas[i + x][j + y].valor for x in range(3) for y in range(3)]):
                    return False

        return True

    def es_secuencia_valida(self, secuencia):
        return set(secuencia) == set(range(1, 10))

    def actualizar_tiempo(self):
        self.tiempo += 1
        minutos, segundos = divmod(self.tiempo, 60)
        self.tiempo_label.setText(f"Tiempo: {minutos:02d}:{segundos:02d}")

    def finalizar_juego(self):
        self.timer.stop()
        minutos, segundos = divmod(self.tiempo, 60)
        mensaje = f"¡Juego terminado!\nTiempo: {minutos:02d}:{segundos:02d}"
        self.mensaje_label.setText(mensaje)