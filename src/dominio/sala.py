from src.dominio.tablero import Tablero

# Gestiona los participantes y mantiene el tablero compartido activo

class Sala:

    def __init__(self):
        self.tablero = Tablero()
        # CA4, CA5 — lista de desarrolladores conectados actualmente
        self.desarrolladores = []

    # CA4 — admite a un desarrollador y le da acceso al tablero actual
    def unirse(self, desarrollador: str):
        self.desarrolladores.append(desarrollador)
        return self.tablero

    # CA5 — elimina al desarrollador pero conserva el tablero intacto
    def salir(self, desarrollador: str):
        self.desarrolladores.remove(desarrollador)