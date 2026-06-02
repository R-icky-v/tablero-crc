from src.dominio.tarjeta_crc import TarjetaCRC


# CA2 — al crear la tarjeta, el nombre de clase queda registrado
def test_tarjeta_almacena_nombre_al_crearse():
    tarjeta = TarjetaCRC("Tablero")
    assert tarjeta.nombre_clase == "Tablero"


# CA3 — al editar la tarjeta, su contenido queda actualizado
def test_tarjeta_actualiza_contenido_al_editarse():
    tarjeta = TarjetaCRC("Tablero")
    tarjeta.editar(
        responsabilidades=["Registrar tarjetas"],
        colaboradores=["TarjetaCRC"]
    )
    assert tarjeta.responsabilidades == ["Registrar tarjetas"]
    assert tarjeta.colaboradores == ["TarjetaCRC"]