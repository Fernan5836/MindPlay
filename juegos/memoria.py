import random
from PyQt6.QtWidgets import (QGridLayout, QPushButton, QMessageBox, QLabel,
                             QVBoxLayout, QHBoxLayout, QWidget)
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from juegos.juego_base import JuegoBase


class CartaBoton(QPushButton):
    # Diccionario de emojis para usar como "imágenes"
    EMOJIS = {
        1: "🐶", 2: "🐱", 3: "🐼", 4: "🐨",
        5: "🦊", 6: "🦁", 7: "🐯", 8: "🐸"
    }

    def __init__(self, valor):
        super().__init__()
        self.valor = valor
        self.esta_volteada = False
        self.esta_emparejada = False
        self._configurar_estilo()

    def _configurar_estilo(self):
        self.setFixedSize(100, 100)
        self.setIconSize(QSize(60, 60))
        self._actualizar_estilo()

    def _actualizar_estilo(self):
        color_fondo = "#4CAF50" if self.esta_emparejada else "#2196F3" if self.esta_volteada else "#3F51B5"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color_fondo};
                border-radius: 15px;
                border: 3px solid #1565C0;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
                border: 3px solid #FFA000;
            }}
            QPushButton:pressed {{
                background-color: #0D47A1;
            }}
        """)

        # Mostrar el contenido según el estado
        if self.esta_volteada or self.esta_emparejada:
            # Usando emojis
            self.setText(self.EMOJIS[self.valor])
            self.setFont(QFont('Segoe UI Emoji', 32))

            # Alternativa: usando imágenes reales
            """
            self.setText("")
            self.setIcon(QIcon(self.IMAGENES[self.valor]))
            """
        else:
            self.setText("?")
            self.setFont(QFont('Arial', 32, QFont.Weight.Bold))
            self.setIcon(QIcon())  # Limpiar el icono si se estaba usando

    def voltear(self):
        self.esta_volteada = not self.esta_volteada
        self._actualizar_estilo()

    def emparejar(self):
        self.esta_emparejada = True
        self._actualizar_estilo()


class JuegoMemoria(JuegoBase):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎮 Juego de Memoria")
        self.setGeometry(100, 100, 600, 700)
        self._configurar_interfaz()

    def _configurar_interfaz(self):
        self.contenedor_principal = QVBoxLayout()
        self.setLayout(self.contenedor_principal)

        # Título
        self.lbl_titulo = QLabel("🧠 Juego de Memoria")
        self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titulo.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.lbl_titulo.setStyleSheet("color: #1565C0; margin: 10px;")
        self.contenedor_principal.addWidget(self.lbl_titulo)

        # Panel superior
        self.panel_superior = QHBoxLayout()
        self.lbl_intentos = QLabel("🎯 Intentos: 0")
        self.lbl_puntuacion = QLabel("⭐ Puntuación: 0")
        self.lbl_tiempo = QLabel("⏱️ Tiempo: 0s")

        for label in [self.lbl_intentos, self.lbl_puntuacion, self.lbl_tiempo]:
            label.setFont(QFont('Arial', 14))
            label.setStyleSheet("""
                color: #1565C0;
                background-color: #E3F2FD;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #1565C0;
            """)
            self.panel_superior.addWidget(label)

        self.contenedor_principal.addLayout(self.panel_superior)

        # Tablero
        self.contenedor_tablero = QWidget()
        self.layout_tablero = QGridLayout()
        self.contenedor_tablero.setLayout(self.layout_tablero)
        self.layout_tablero.setSpacing(10)
        self.layout_tablero.setContentsMargins(20, 20, 20, 20)
        self.contenedor_tablero.setStyleSheet("""
            QWidget {
                background-color: #E3F2FD;
                border-radius: 20px;
            }
        """)
        self.contenedor_principal.addWidget(self.contenedor_tablero)

        # Variables del juego
        self.cartas = []
        self.carta_volteada = None
        self.puede_voltear = True
        self.pares_encontrados = 0
        self.intentos = 0
        self.tiempo = 0

        # Timer para el tiempo
        self.timer = QTimer()
        self.timer.timeout.connect(self._actualizar_tiempo)

    def iniciar_juego(self):
        self.puntuacion = 0
        self.pares_encontrados = 0
        self.intentos = 0
        self.tiempo = 0
        self._actualizar_etiquetas()
        self.crear_tablero()
        self.timer.start(1000)

    def crear_tablero(self):
        # Limpiar tablero anterior
        for carta in self.cartas:
            self.layout_tablero.removeWidget(carta)
            carta.deleteLater()
        self.cartas.clear()

        valores = list(range(1, 9)) * 2
        random.shuffle(valores)

        for i in range(4):
            for j in range(4):
                carta = CartaBoton(valores.pop())
                carta.clicked.connect(lambda checked, c=carta: self.voltear_carta(c))
                self.layout_tablero.addWidget(carta, i, j)
                self.cartas.append(carta)

    def voltear_carta(self, carta):
        if (not self.puede_voltear or carta.esta_volteada or
                carta.esta_emparejada):
            return

        carta.voltear()

        if self.carta_volteada is None:
            self.carta_volteada = carta
        else:
            self.puede_voltear = False
            self.intentos += 1
            self._actualizar_etiquetas()

            if self.carta_volteada.valor == carta.valor:
                self._procesar_coincidencia(carta)
            else:
                QTimer.singleShot(1000, lambda: self._ocultar_cartas(self.carta_volteada, carta))

    def _procesar_coincidencia(self, carta):
        self.pares_encontrados += 1
        self.puntuacion += max(20 - self.intentos, 5)
        self.carta_volteada.emparejar()
        carta.emparejar()
        self.carta_volteada = None
        self.puede_voltear = True
        self._actualizar_etiquetas()

        if self.pares_encontrados == 8:
            self.finalizar_juego()

    def _ocultar_cartas(self, carta1, carta2):
        carta1.voltear()
        carta2.voltear()
        self.carta_volteada = None
        self.puede_voltear = True

    def _actualizar_etiquetas(self):
        self.lbl_intentos.setText(f"🎯 Intentos: {self.intentos}")
        self.lbl_puntuacion.setText(f"⭐ Puntuación: {self.puntuacion}")
        self.lbl_tiempo.setText(f"⏱️ Tiempo: {self.tiempo}s")

    def _actualizar_tiempo(self):
        self.tiempo += 1
        self.lbl_tiempo.setText(f"⏱️ Tiempo: {self.tiempo}s")

    def finalizar_juego(self):
        self.timer.stop()
        mensaje = (f"🎉 ¡Felicidades! Has completado el juego.\n\n"
                   f"Estadísticas finales:\n"
                   f"🎯 Intentos: {self.intentos}\n"
                   f"⭐ Puntuación: {self.puntuacion}\n"
                   f"⏱️ Tiempo: {self.tiempo} segundos")

        QMessageBox.information(self, "🏆 ¡Fin del juego!", mensaje)
        self.close()