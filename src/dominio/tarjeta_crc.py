# Objeto central del sistema: representa una tarjeta CRC del tablero

class TarjetaCRC:

    # CA2 — almacena el nombre de clase al momento de su creación
    def __init__(self, nombre_clase: str):
        self.nombre_clase = nombre_clase
        self.responsabilidades = []
        self.colaboradores = []

    # CA3 — permite actualizar el contenido de la tarjeta al ser editada
    def editar(self, responsabilidades: list, colaboradores: list):
        self.responsabilidades = responsabilidades
        self.colaboradores = colaboradores