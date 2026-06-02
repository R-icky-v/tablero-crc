import datetime
from src.dominio.tarea_completada import TareaCompletada
from src.dominio.desarrollador import Desarrollador


# CS1, CS2 — los puntos del día se suman correctamente
def test_desarrollador_suma_puntos_del_dia():
    dev = Desarrollador("Carlos")
    dev.registrar_tarea(TareaCompletada("Carlos", 4, datetime.date.today(), "Tablero"))
    dev.registrar_tarea(TareaCompletada("Carlos", 3, datetime.date.today(), "Sala"))
    assert dev.sumar_puntos_hoy() == 7


# CS2 — se visualizan las tarjetas CRC implementadas por el desarrollador
def test_desarrollador_expone_tarjetas_implementadas():
    dev = Desarrollador("Carlos")
    dev.registrar_tarea(TareaCompletada("Carlos", 4, datetime.date.today(), "Tablero"))
    dev.registrar_tarea(TareaCompletada("Carlos", 3, datetime.date.today(), "Sala"))
    assert "Tablero" in dev.tarjetas_implementadas()
    assert "Sala"    in dev.tarjetas_implementadas()