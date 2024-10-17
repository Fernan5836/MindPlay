from PyQt6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QLabel, QHBoxLayout, QFrame, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from juegos.memoria import JuegoMemoria
from juegos.calculo_rapido import JuegoCalculoRapido
from juegos.reconocimiento_patrones import JuegoReconocimientoPatrones
from juegos.sudoku import JuegoSudoku
from functools import partial


class TarjetaJuego(QFrame):
    def __init__(self, titulo, descripcion, icono, on_click):
        super().__init__()
        self.setFixedSize(200, 250)
        self.setup_ui(titulo, descripcion, icono, on_click)

    def setup_ui(self, titulo, descripcion, icono, on_click):
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 15px;
                border: 2px solid #E0E0E0;
            }
            QFrame:hover {
                border: 2px solid #2196F3;
                background-color: #F5F5F5;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Icono
        icono_label = QLabel()
        icono_label.setStyleSheet(f"""
            QLabel {{
                background-color: {icono['color']};
                border-radius: 25px;
                padding: 10px;
            }}
        """)
        icono_label.setFixedSize(50, 50)
        icono_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icono_label.setText(icono['emoji'])
        icono_label.setFont(QFont('Segoe UI Emoji', 20))

        # Título
        titulo_label = QLabel(titulo)
        titulo_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        titulo_label.setStyleSheet("color: #1565C0;")
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Descripción
        desc_label = QLabel(descripcion)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #757575;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botón Jugar
        boton_jugar = QPushButton("¡Jugar!")
        boton_jugar.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        boton_jugar.clicked.connect(on_click)

        layout.addWidget(icono_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        layout.addWidget(boton_jugar)

        self.setLayout(layout)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎮 MindPlay - Juegos Mentales")
        self.setGeometry(100, 100, 900, 600)
        self.setup_ui()

    def setup_ui(self):
        # Widget y layout principal
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Estilo general
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
        """)

        # Cabecera
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background-color: #1565C0;
                border-radius: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_widget)

        # Título principal
        titulo = QLabel("🎮 MindPlay")
        titulo.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtítulo
        subtitulo = QLabel("Entrena tu mente mientras te diviertes")
        subtitulo.setFont(QFont('Arial', 14))
        subtitulo.setStyleSheet("color: #E3F2FD;")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(titulo)
        header_layout.addWidget(subtitulo)

        # Área de juegos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        juegos_widget = QWidget()
        juegos_layout = QGridLayout(juegos_widget)
        juegos_layout.setSpacing(20)

        juegos = [
            {
                "titulo": "Memoria",
                "clase": JuegoMemoria,
                "descripcion": "Ejercita tu memoria encontrando pares de cartas coincidentes.",
                "icono": {"emoji": "🧠", "color": "#E3F2FD"}
            },
            {
                "titulo": "Cálculo Rápido",
                "clase": JuegoCalculoRapido,
                "descripcion": "Pon a prueba tu agilidad mental resolviendo operaciones matemáticas.",
                "icono": {"emoji": "🔢", "color": "#E8F5E9"}
            },
            {
                "titulo": "Reconocimiento de Patrones",
                "clase": JuegoReconocimientoPatrones,
                "descripcion": "Desarrolla tu capacidad de identificar patrones y secuencias.",
                "icono": {"emoji": "👁️", "color": "#FFF3E0"}
            },
            {
                "titulo": "Sudoku",
                "clase": JuegoSudoku,
                "descripcion": "Resuelve el clásico rompecabezas numérico japonés.",
                "icono": {"emoji": "🎲", "color": "#F3E5F5"}
            }
        ]

        # Crear tarjetas de juegos
        for i, juego in enumerate(juegos):
            tarjeta = TarjetaJuego(
                juego["titulo"],
                juego["descripcion"],
                juego["icono"],
                partial(self.abrir_juego, juego["clase"])
            )
            juegos_layout.addWidget(tarjeta, i // 2, i % 2)

        scroll_area.setWidget(juegos_widget)

        # Agregar widgets al layout principal
        main_layout.addWidget(header_widget)
        main_layout.addWidget(scroll_area)

        self.setCentralWidget(main_widget)

    def abrir_juego(self, clase_juego):
        if hasattr(self, 'juego_actual'):
            self.juego_actual.close()
        self.juego_actual = clase_juego()
        self.juego_actual.show()
        if hasattr(self.juego_actual, 'iniciar_juego'):
            self.juego_actual.iniciar_juego()

    def closeEvent(self, event):
        # Cerrar juego actual si existe
        if hasattr(self, 'juego_actual'):
            self.juego_actual.close()
        event.accept()