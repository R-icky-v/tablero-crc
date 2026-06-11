import datetime
from src.dominio.tarea_completada import TareaCompletada

# CS1, CS2 — representa a un desarrollador y sus contribuciones

class Desarrollador:

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tareas = []

    # CS1 — registra una tarea completada por el desarrollador
    def registrar_tarea(self, tarea: TareaCompletada):
        self.tareas.append(tarea)

    # CS2 — puntos acumulados hoy (vista diaria)
    def sumar_puntos_hoy(self) -> int:
        hoy = datetime.date.today()
        return sum(t.puntos for t in self.tareas if t.fecha == hoy)

    # CS2 — puntos acumulados en toda la iteración
    def sumar_puntos_total(self) -> int:
        return sum(t.puntos for t in self.tareas)

    # CS2 — tarjetas CRC implementadas en toda la iteración
    def tarjetas_implementadas(self) -> list:
        return [t.tarjeta_crc for t in self.tareas]