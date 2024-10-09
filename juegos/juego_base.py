from PyQt6.QtWidgets import QWidget
from abc import ABC, abstractmethod

class JuegoBaseMeta(type(QWidget), type(ABC)):
    pass

class JuegoBase(QWidget, ABC, metaclass=JuegoBaseMeta):
    def __init__(self):
        super().__init__()
        self.puntuacion = 0

    @abstractmethod
    def iniciar_juego(self):
        pass

    @abstractmethod
    def finalizar_juego(self):
        pass

    def actualizar_puntuacion(self, puntos):
        self.puntuacion += puntos