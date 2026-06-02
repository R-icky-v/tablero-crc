from fastapi import WebSocket

# Administra las conexiones WebSocket activas en la sala

class GestorConexiones:

    def __init__(self):
        # CA1, CA3 — lista de clientes conectados para difundir eventos
        self.conexiones_activas: list[WebSocket] = []

    # acepta la conexión y la registra
    async def conectar(self, websocket: WebSocket):
        await websocket.accept()
        self.conexiones_activas.append(websocket)

    # CA5 — elimina la conexión al desconectarse el desarrollador
    def desconectar(self, websocket: WebSocket):
        if websocket in self.conexiones_activas:
            self.conexiones_activas.remove(websocket)

    # CA1, CA3 — envía un mensaje a todos los conectados
    async def difundir(self, mensaje: dict):
        for conexion in self.conexiones_activas:
            await conexion.send_json(mensaje)