import src.infraestructura.app as app_module
from src.dominio.tarjeta_crc import TarjetaCRC
from starlette.testclient import TestClient
from src.infraestructura.app import app


# CA4 — al conectarse, el participante recibe las tarjetas actuales
def test_al_unirse_recibe_tarjetas_actuales():
    app_module.sala.tablero.agregar_tarjeta(TarjetaCRC("Tablero"))
    client = TestClient(app)
    with client.websocket_connect("/sala") as ws:
        respuesta = ws.receive_json()
        assert respuesta["evento"] == "sala_actual"
        assert respuesta["tarjetas"][0]["nombre_clase"] == "Tablero"


# CA1 — al crear una tarjeta, el servidor la difunde a los participantes
def test_crear_tarjeta_difunde_evento():
    client = TestClient(app)
    with client.websocket_connect("/sala") as ws:
        ws.receive_json()  # consumir sala_actual
        ws.send_json({"accion": "crear_tarjeta", "nombre_clase": "TarjetaCRC"})
        respuesta = ws.receive_json()
        assert respuesta["evento"]      == "tarjeta_creada"
        assert respuesta["nombre_clase"] == "TarjetaCRC"


# CA3 — al editar una tarjeta, el servidor difunde el cambio actualizado
def test_editar_tarjeta_difunde_evento():
    app_module.sala.tablero.agregar_tarjeta(TarjetaCRC("Tablero"))
    client = TestClient(app)
    with client.websocket_connect("/sala") as ws:
        ws.receive_json()  # consumir sala_actual
        ws.send_json({
            "accion":            "editar_tarjeta",
            "indice":            0,
            "responsabilidades": ["Registrar tarjetas"],
            "colaboradores":     ["TarjetaCRC"]
        })
        respuesta = ws.receive_json()
        assert respuesta["evento"]           == "tarjeta_editada"
        assert respuesta["responsabilidades"] == ["Registrar tarjetas"]


# CA5 — al desconectarse, las tarjetas permanecen en la sala
def test_salir_conserva_tarjetas_en_sala():
    client = TestClient(app)
    with client.websocket_connect("/sala") as ws:
        ws.receive_json()  # consumir sala_actual
        ws.send_json({"accion": "crear_tarjeta", "nombre_clase": "Sala"})
        ws.receive_json()  # consumir tarjeta_creada
    assert len(app_module.sala.tablero.obtener_tarjetas()) == 1


# CS1 — al registrar una tarea, el servidor la difunde a todos
def test_registrar_tarea_difunde_evento():
    client = TestClient(app)
    with client.websocket_connect("/sala") as ws:
        ws.receive_json()  # consumir sala_actual
        ws.send_json({
            "accion":      "registrar_tarea",
            "nombre_dev":  "Carlos",
            "puntos":      5,
            "tarjeta_crc": "Tablero"
        })
        respuesta = ws.receive_json()
        assert respuesta["evento"]      == "tarea_registrada"
        assert respuesta["nombre_dev"]  == "Carlos"
        assert respuesta["puntos"]      == 5
        assert respuesta["tarjeta_crc"] == "Tablero"


# CS2 — al consultar contribuciones, devuelve puntos y tarjetas por desarrollador
def test_consultar_contribuciones_devuelve_datos():
    client = TestClient(app)
    with client.websocket_connect("/sala") as ws:
        ws.receive_json()  # consumir sala_actual
        ws.send_json({
            "accion": "registrar_tarea",
            "nombre_dev": "Ana", "puntos": 8, "tarjeta_crc": "Sala"
        })
        ws.receive_json()  # consumir tarea_registrada
        ws.send_json({"accion": "consultar_contribuciones"})
        respuesta = ws.receive_json()
        assert respuesta["evento"] == "contribuciones"
        assert "Ana" in respuesta["contribuciones"]
        assert respuesta["contribuciones"]["Ana"]["puntos_hoy"] == 8


# CS3, CS4 — al consultar avance, devuelve porcentaje y déficit
def test_consultar_avance_devuelve_porcentaje_y_deficit():
    client = TestClient(app)
    with client.websocket_connect("/sala") as ws:
        ws.receive_json()  # consumir sala_actual
        ws.send_json({
            "accion": "registrar_tarea",
            "nombre_dev": "Carlos", "puntos": 10, "tarjeta_crc": "Tablero"
        })
        ws.receive_json()  # consumir tarea_registrada
        ws.send_json({"accion": "consultar_avance", "dias_transcurridos": 1})
        respuesta = ws.receive_json()
        assert respuesta["evento"]     == "avance"
        assert respuesta["porcentaje"] == 10.0
        assert respuesta["puntos_hoy"] == 10