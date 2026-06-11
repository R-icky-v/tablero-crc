#src/dominio/tarea_completada.py
import datetime

# CS1 — representa una tarea finalizada por un desarrollador

class TareaCompletada:

    # CS1 — registra nombre del dev, puntos, fecha y la tarjeta CRC implementada
    def __init__(self, nombre_dev: str, puntos: int, fecha: datetime.date, tarjeta_crc: str):
        self.nombre_dev  = nombre_dev
        self.puntos      = puntos
        self.fecha       = fecha
        self.tarjeta_crc = tarjeta_crc  # CS1 — tarjeta CRC que implementó