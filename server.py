# import asyncio
# import websockets
# import nest_asyncio
# import os

# nest_asyncio.apply()

# clients = set()

# async def handler(websocket, path):
#     clients.add(websocket)
#     print("Client connected")
#     try:
#         async for message in websocket:
#             print(f"Received message from client: {message}")
#             if message == "capture":
#                 try:
#                     print("Received 'capture' command from client")
#                     await websocket.send("Capture command received")
#                     print("Sent confirmation for capture command")
#                 except Exception as e:
#                     print(f"Error receiving/sending frame data: {e}")
#     except websockets.ConnectionClosed as e:
#         print(f"Connection closed: {e}")
#     except Exception as e:
#         print(f"General error: {e}")
#     finally:
#         clients.remove(websocket)
#         print("Client disconnected")

# async def periodic_ping():
#     while True:
#         await asyncio.sleep(30)  # Increase the interval between pings
#         for websocket in list(clients):  # Create a copy of the set for iteration
#             try:
#                 await websocket.ping()
#                 print("Ping sent")
#             except Exception as e:
#                 print(f"Error sending ping: {e}")

# port = int(os.environ.get("PORT", 10000))
# start_server = websockets.serve(handler, "0.0.0.0", port)

# print(f"Server started on port {port}")
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().create_task(periodic_ping())
# asyncio.get_event_loop().run_forever()



import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

start_server = websockets.serve(echo, "0.0.0.0", 10000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
