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



# import asyncio
# import websockets

# async def echo(websocket, path):
#     async for message in websocket:
#         await websocket.send(message)

# # Use default port for HTTPS (Render handles SSL/TLS termination)
# start_server = websockets.serve(echo, "0.0.0.0", 10000)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

# import asyncio
# import websockets
# import nest_asyncio
# from io import BytesIO
# from PIL import Image, UnidentifiedImageError
# import base64

# nest_asyncio.apply()

# clients = set()

# def is_valid_image(image_bytes):
#     try:
#         image = Image.open(BytesIO(image_bytes))
#         image.verify()  # Verify that it is, in fact, an image
#         return True
#     except (UnidentifiedImageError, IOError):
#         print("Invalid image")
#         return False

# async def handler(websocket, path):
#     clients.add(websocket)
#     print("Client connected")
#     try:
        # async for message in websocket:
        #     print(f"Received message of length: {len(message)}")

        #     if len(message) > 1000:  # Assuming a minimum size for image frames
        #         if is_valid_image(message):
        #             # Reopen the image since verify() destroys it
        #             image = Image.open(BytesIO(message))
        #             buffered = BytesIO()
        #             image.save(buffered, format="JPEG")
        #             img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        #             # Broadcast the image to all connected clients
        #             for client in clients:
        #                 try:
        #                     await client.send(img_str)
        #                 except Exception as e:
        #                     print(f"Error sending image: {e}")
        #         else:
        #             print("Invalid image received")
        #     else:
        #         print(f"Received non-image message: {message}")
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
import nest_asyncio
import os
from io import BytesIO
from PIL import Image
import base64
import cv2

nest_asyncio.apply()

clients = set()

def is_valid_image(data):
    try:
        image = Image.open(BytesIO(data))
        image.verify()  # Verify the image to check for corruption
        return True
    except Exception as e:
        print(f"Image validation error: {e}")
        return False

async def handler(websocket, path):
    clients.add(websocket)
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received message of length: {len(message)}")

            if len(message) > 1000:  # Assuming a minimum size for image frames
                if is_valid_image(message):
                    # Reopen the image since verify() destroys it
                    image = Image.open(BytesIO(message))
                    buffered = BytesIO()
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

                    # Broadcast the image to all connected clients
                    for client in clients:
                        try:
                            await client.send(img_str)
                        except Exception as e:
                            print(f"Error sending image: {e}")
                else:
                    print("Invalid image received")
            else:
                print(f"Received non-image message: {message}")

            if message == "capture":
                try:
                    print("Received 'capture' command from client")

                    # Capture image using OpenCV
                    cap = cv2.VideoCapture(0)
                    ret, frame = cap.read()
                    cap.release()

                    if not ret:
                        print("Failed to capture image")
                        await websocket.send("Failed to capture image")
                        continue

                    # Convert the captured image to JPEG
                    _, buffer = cv2.imencode('.jpg', frame)
                    img_str = base64.b64encode(buffer).decode('utf-8')
                    
                    # Send the image data to the client
                    await websocket.send(img_str)
                    print("Sent image data to client")
                except Exception as e:
                    print(f"Error sending image data: {e}")
            
    except websockets.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        clients.remove(websocket)
        print("Client disconnected")

async def periodic_ping():
    while True:
        await asyncio.sleep(30)  # Increase the interval between pings
        for websocket in list(clients):  # Create a copy of the set for iteration
            try:
                await websocket.ping()
                print("Ping sent")
            except Exception as e:
                print(f"Error sending ping: {e}")

port = int(os.environ.get("PORT", 10000))
start_server = websockets.serve(handler, "0.0.0.0", port)

print(f"Server started on port {port}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().create_task(periodic_ping())
asyncio.get_event_loop().run_forever()
