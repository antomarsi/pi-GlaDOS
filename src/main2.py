import asyncio
import websockets
import logging
import json
from camera_system import CameraSystem
from utils import start_component

PORT = 5678

LOG_LEVEL = "INFO"

logging.basicConfig(level=LOG_LEVEL)

sockets = set()
modules = []

loop = asyncio.get_event_loop()




async def on_track(camera):
    message = {
        "faces": camera.faces
    }
    for socket in sockets:
        await socket.send(json.dumps(message))

start_camera = start_component(CameraSystem(sockets), [on_track])
modules.append(start_camera)


async def on_connect(socket, path):
    logging.info("Socket connected...")
    sockets.add(socket)
    try:
        while True:
            message = await socket.recv()
            logging.warning('Ignoring received message: {}'.format(message))
            for module in modules:
                await start_camera.handle_message(sockets, message)
    except:
        sockets.remove(socket)
        logging.info(
            "Socket disconnected (maybe in response to closing handshake)...")

async def client():
    uri = "ws://localhost:{}".format(PORT)
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"< {message}")

if __name__ == "__main__":
    logging.debug("Starting capture loop...")
    logging.debug("Starting websocket...")
    start_server = websockets.serve(on_connect, port=PORT)
    loop.run_until_complete(start_camera)
    loop.run_until_complete(start_server)
    loop.run_until_complete(client())
    logging.info("Started ... ")
    loop.run_forever()
