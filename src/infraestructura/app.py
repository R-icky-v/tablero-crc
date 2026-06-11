#Infraestructura
#1.- src/infraestructura/app.py
import datetime
import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from ..dominio.tarjeta_crc import TarjetaCRC
from ..dominio.sala import Sala
from ..dominio.desarrollador import Desarrollador
from ..dominio.tarea_completada import TareaCompletada
from ..dominio.iteracion import Iteracion
from ..dominio.ritmo_equipo import RitmoEquipo
from .gestor_conexiones import GestorConexiones

load_dotenv()
GROQ_KEY = os.environ.get("GROQ_KEY", "")

app = FastAPI()

# estado compartido — persiste entre conexiones
sala    = Sala()
gestor  = GestorConexiones()

# CS3, CS4 — iteración con 100 puntos en 10 días (configurable)
iteracion    = Iteracion(100, 10)
ritmo_equipo = RitmoEquipo(iteracion)
desarrolladores: dict[str, Desarrollador] = {}

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.websocket("/sala")
async def endpoint_sala(websocket: WebSocket):
    await gestor.conectar(websocket)
    dev_id  = str(id(websocket))
    tablero = sala.unirse(dev_id)

    # CA4 — enviar tarjetas actuales al nuevo participante
    tarjetas_actuales = [
        {
            "nombre_clase":      t.nombre_clase,
            "responsabilidades": t.responsabilidades,
            "colaboradores":     t.colaboradores
        }
        for t in tablero.obtener_tarjetas()


    ]

    await websocket.send_json({
        "evento":    "config",
        "groq_key":  GROQ_KEY
    })
    
    await websocket.send_json({"evento": "sala_actual", "tarjetas": tarjetas_actuales})

    try:
        while True:
            data   = await websocket.receive_json()
            accion = data.get("accion")

            # ── US1 ──────────────────────────────────────────────

            if accion == "crear_tarjeta":
                # CA1 — registrar tarjeta y difundir a todos
                tarjeta = TarjetaCRC(data["nombre_clase"])
                tablero.agregar_tarjeta(tarjeta)
                await gestor.difundir({
                    "evento":            "tarjeta_creada",
                    "nombre_clase":      tarjeta.nombre_clase,
                    "responsabilidades": tarjeta.responsabilidades,
                    "colaboradores":     tarjeta.colaboradores
                })

            elif accion == "editar_tarjeta":
                # CA3 — editar tarjeta y difundir cambio a todos
                indice  = data["indice"]
                tarjeta = tablero.obtener_tarjetas()[indice]
                tarjeta.editar(data["responsabilidades"], data["colaboradores"])
                await gestor.difundir({
                    "evento":            "tarjeta_editada",
                    "indice":            indice,
                    "nombre_clase":      tarjeta.nombre_clase,
                    "responsabilidades": tarjeta.responsabilidades,
                    "colaboradores":     tarjeta.colaboradores
                })

            # ── US2 ──────────────────────────────────────────────

            elif accion == "registrar_tarea":
                # CS1 — registrar tarea completada y difundir a todos
                nombre_dev  = data["nombre_dev"]
                puntos      = data["puntos"]
                tarjeta_crc = data["tarjeta_crc"]

                if nombre_dev not in desarrolladores:
                    desarrolladores[nombre_dev] = Desarrollador(nombre_dev)

                tarea = TareaCompletada(
                    nombre_dev,
                    puntos,
                    datetime.date.today(),
                    tarjeta_crc
                )
                desarrolladores[nombre_dev].registrar_tarea(tarea)
                ritmo_equipo.registrar_tarea_equipo(tarea)

                await gestor.difundir({
                    "evento":      "tarea_registrada",
                    "nombre_dev":  nombre_dev,
                    "puntos":      puntos,
                    "tarjeta_crc": tarjeta_crc
                })

            elif accion == "consultar_contribuciones":
                # CS2 — puntos totales de la iteración por desarrollador
                contribuciones = {
                    nombre: {
                        "puntos_hoy":             dev.sumar_puntos_hoy(),
                        "puntos_total":           dev.sumar_puntos_total(),  # ← nuevo
                        "tarjetas_implementadas": dev.tarjetas_implementadas()
                    }
                    for nombre, dev in desarrolladores.items()
                }
                await websocket.send_json({
                    "evento":         "contribuciones",
                    "contribuciones": contribuciones
                })

            elif accion == "consultar_avance":
                # CS3, CS4 — total acumulado en iteración, no solo hoy
                dias = data.get("dias_transcurridos", 1)
                await websocket.send_json({
                    "evento":       "avance",
                    "porcentaje":   ritmo_equipo.calcular_porcentaje_avance(),
                    "deficit":      ritmo_equipo.calcular_deficit(dias),
                    "puntos_hoy":   ritmo_equipo.puntos_equipo_hoy(),
                    "puntos_total": ritmo_equipo.puntos_totales_equipo()  # ← nuevo
                })
            
            

    except WebSocketDisconnect:
        # CA5 — desarrollador sale, el tablero y sus tarjetas permanecen
        gestor.desconectar(websocket)
        sala.salir(dev_id)