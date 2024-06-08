import asyncio
import websockets
import nest_asyncio
import os

nest_asyncio.apply()

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            if message == "capture":
                frame_data = await websocket.recv()
                for client in clients:
                    if client != websocket:
                        await client.send(frame_data)
    finally:
        clients.remove(websocket)

start_server = websockets.serve(handler, "0.0.0.0", int(os.environ.get("PORT", 5000)))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
