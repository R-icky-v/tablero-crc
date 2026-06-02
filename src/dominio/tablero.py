# Contiene y gestiona todas las tarjetas CRC de la sala

class Tablero:

    def __init__(self):
        # CA1, CA4 — lista que persiste las tarjetas del tablero
        self.tarjetas = []

    # CA1 — registra una nueva tarjeta al ser creada
    def agregar_tarjeta(self, tarjeta):
        self.tarjetas.append(tarjeta)

    # CA4 — entrega todas las tarjetas con su contenido actual
    def obtener_tarjetas(self):
        return self.tarjetas