from src.dominio.tarjeta_crc import TarjetaCRC
from src.dominio.sala import Sala


# CA4 — al unirse, el desarrollador recibe el tablero con las tarjetas actuales
def test_sala_da_acceso_al_tablero_al_unirse():
    sala = Sala()
    tarjeta = TarjetaCRC("Tablero")
    sala.tablero.agregar_tarjeta(tarjeta)

    tablero_recibido = sala.unirse("dev1")

    assert tarjeta in tablero_recibido.obtener_tarjetas()


# CA5 — al salir un desarrollador, las tarjetas permanecen en el tablero
def test_sala_conserva_tarjetas_cuando_desarrollador_sale():
    sala = Sala()
    tarjeta = TarjetaCRC("Tablero")
    sala.tablero.agregar_tarjeta(tarjeta)
    sala.unirse("dev1")

    sala.salir("dev1")

    assert tarjeta in sala.tablero.obtener_tarjetas()


# CA5 — al salir un desarrollador, los demás siguen conectados
def test_sala_mantiene_otros_desarrolladores_al_salir_uno():
    sala = Sala()
    sala.unirse("dev1")
    sala.unirse("dev2")

    sala.salir("dev1")

    assert "dev2" in sala.desarrolladores
    assert "dev1" not in sala.desarrolladores