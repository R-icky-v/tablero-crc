import datetime
from src.dominio.tarea_completada import TareaCompletada


# CS1 — al completar una tarea, los puntos quedan registrados correctamente
def test_tarea_registra_puntos_correctamente():
    tarea = TareaCompletada("Carlos", 5, datetime.date.today(), "Tablero")
    assert tarea.puntos == 5


# CS1 — al completar una tarea, la TarjetaCRC implementada queda registrada
def test_tarea_registra_tarjeta_crc_implementada():
    tarea = TareaCompletada("Carlos", 5, datetime.date.today(), "Tablero")
    assert tarea.tarjeta_crc == "Tablero"