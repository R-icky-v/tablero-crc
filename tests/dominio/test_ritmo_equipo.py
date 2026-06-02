import datetime
from src.dominio.tarea_completada import TareaCompletada
from src.dominio.iteracion import Iteracion
from src.dominio.ritmo_equipo import RitmoEquipo


# CS2 — los puntos totales del equipo en el día se calculan correctamente
def test_ritmo_equipo_suma_puntos_del_dia():
    iteracion = Iteracion(100, 10)
    ritmo = RitmoEquipo(iteracion)
    ritmo.registrar_tarea_equipo(TareaCompletada("Carlos", 4, datetime.date.today(), "Tablero"))
    ritmo.registrar_tarea_equipo(TareaCompletada("Ana",    6, datetime.date.today(), "Sala"))
    assert ritmo.puntos_equipo_hoy() == 10


# CS3 — el porcentaje de avance se calcula correctamente
def test_ritmo_equipo_calcula_porcentaje_avance():
    iteracion = Iteracion(100, 10)
    ritmo = RitmoEquipo(iteracion)
    ritmo.registrar_tarea_equipo(TareaCompletada("Carlos", 25, datetime.date.today(), "Tablero"))
    assert ritmo.calcular_porcentaje_avance() == 25.0


# CS4 — se detecta déficit cuando el ritmo real va por debajo del esperado
def test_ritmo_equipo_detecta_deficit_cuando_va_atrasado():
    iteracion = Iteracion(100, 10)
    ritmo = RitmoEquipo(iteracion)
    ritmo.registrar_tarea_equipo(TareaCompletada("Carlos", 15, datetime.date.today(), "Tablero"))
    assert ritmo.calcular_deficit(dias_transcurridos=2) == 5


# CS4 — el déficit es cero cuando el ritmo va a buen ritmo
def test_ritmo_equipo_deficit_es_cero_si_va_bien():
    iteracion = Iteracion(100, 10)
    ritmo = RitmoEquipo(iteracion)
    ritmo.registrar_tarea_equipo(TareaCompletada("Carlos", 25, datetime.date.today(), "Tablero"))
    assert ritmo.calcular_deficit(dias_transcurridos=2) == 0