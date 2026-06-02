from src.dominio.tarjeta_crc import TarjetaCRC
from src.dominio.tablero import Tablero


# CA1 — al agregar una tarjeta, esta aparece en el tablero
def test_tablero_registra_tarjeta_al_agregarla():
    tablero = Tablero()
    tarjeta = TarjetaCRC("Tablero")

    tablero.agregar_tarjeta(tarjeta)

    assert tarjeta in tablero.obtener_tarjetas()


# CA4 — al obtener tarjetas, el contenido actual de cada una es visible
def test_tablero_entrega_contenido_actual_de_tarjetas():
    tablero = Tablero()
    tarjeta = TarjetaCRC("Tablero")
    tablero.agregar_tarjeta(tarjeta)

    # se edita la tarjeta después de agregarla al tablero
    tarjeta.editar(
        responsabilidades=["Registrar tarjetas"],
        colaboradores=["TarjetaCRC"]
    )

    tarjeta_en_tablero = tablero.obtener_tarjetas()[0]
    assert tarjeta_en_tablero.responsabilidades == ["Registrar tarjetas"]


# CA3 — al editar una tarjeta, el tablero refleja el cambio actualizado
def test_tablero_refleja_cambio_al_editar_tarjeta():
    tablero = Tablero()
    tarjeta = TarjetaCRC("Sala")
    tablero.agregar_tarjeta(tarjeta)

    tarjeta.editar(
        responsabilidades=["Admitir desarrolladores"],
        colaboradores=["Tablero"]
    )

    tarjeta_en_tablero = tablero.obtener_tarjetas()[0]
    assert tarjeta_en_tablero.responsabilidades == ["Admitir desarrolladores"]