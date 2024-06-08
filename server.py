import asyncio
import websockets
import nest_asyncio
import os

nest_asyncio.apply()

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            if message == "capture":
                try:
                    frame_data = await websocket.recv()
                    print("Received frame data")
                    for client in clients:
                        if client != websocket:
                            await client.send(frame_data)
                            print("Sent frame data to client")
                except Exception as e:
                    print(f"Error receiving/sending frame data: {e}")
    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        clients.remove(websocket)
        print("Client disconnected")

async def periodic_ping():
    while True:
        await asyncio.sleep(10)
        for websocket in clients:
            try:
                await websocket.ping()
                print("Ping sent")
            except Exception as e:
                print(f"Error sending ping: {e}")

start_server = websockets.serve(handler, "0.0.0.0", int(os.environ.get("PORT", 5000)))

print("Server started")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().create_task(periodic_ping())
asyncio.get_event_loop().run_forever()
