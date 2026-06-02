import datetime
from src.dominio.iteracion import Iteracion
from src.dominio.tarea_completada import TareaCompletada

# CS3, CS4 — calcula el avance del equipo y detecta déficit

class RitmoEquipo:

    def __init__(self, iteracion: Iteracion):
        self.iteracion         = iteracion
        self.tareas_del_equipo = []

    # CS1 — registra una tarea completada al equipo
    def registrar_tarea_equipo(self, tarea: TareaCompletada):
        self.tareas_del_equipo.append(tarea)

    # CS2 — retorna puntos acumulados por el equipo en el día de hoy
    def puntos_equipo_hoy(self) -> int:
        hoy = datetime.date.today()
        return sum(t.puntos for t in self.tareas_del_equipo if t.fecha == hoy)

    # CS3 — calcula el porcentaje de avance respecto al total planificado
    def calcular_porcentaje_avance(self) -> float:
        if self.iteracion.puntos_totales == 0:
            return 0.0
        return (self.puntos_equipo_hoy() / self.iteracion.puntos_totales) * 100

    # CS4 — detecta y retorna el déficit si el ritmo real va por debajo del esperado
    def calcular_deficit(self, dias_transcurridos: int) -> float:
        puntos_por_dia   = self.iteracion.puntos_totales / self.iteracion.dias_totales
        puntos_esperados = puntos_por_dia * dias_transcurridos
        puntos_reales    = self.puntos_equipo_hoy()

        if puntos_reales < puntos_esperados:
            return puntos_esperados - puntos_reales
        return 0