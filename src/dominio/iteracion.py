# CS3, CS4 — mantiene los datos planificados de la iteración

class Iteracion:

    # CS3, CS4 — puntos totales y días planificados de la iteración
    def __init__(self, puntos_totales: int, dias_totales: int):
        self.puntos_totales = puntos_totales
        self.dias_totales   = dias_totales