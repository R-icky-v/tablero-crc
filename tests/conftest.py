import pytest
import src.infraestructura.app as app_module
from src.dominio.sala import Sala
from src.dominio.iteracion import Iteracion
from src.dominio.ritmo_equipo import RitmoEquipo
from src.infraestructura.gestor_conexiones import GestorConexiones


# reinicia todo el estado global antes de cada test
@pytest.fixture(autouse=True)
def reset_estado():
    app_module.sala            = Sala()
    app_module.gestor          = GestorConexiones()
    app_module.iteracion       = Iteracion(100, 10)
    app_module.ritmo_equipo    = RitmoEquipo(app_module.iteracion)
    app_module.desarrolladores = {}