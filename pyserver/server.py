import asyncio
import functools

import websockets
from cbor2 import loads, dumps

from core import Server
from noodle_objects import Method, Signal


starting_state = {
    "methods": {
        (0, 0): Method((0,0), "Test Method 1"),
        (1, 0): Method((0,0), "Test Method 2"),
        (2, 0): Method((0,0), "Test Method 3"),
        (3, 0): Method((0,0), "Test Method 4"),
    }
}

async def send(websocket, message: dict):
    """Send CBOR message using websocket"""
    
    print(f"Sending Message: {message}")
    await websocket.send(dumps(message))


async def handle_client(websocket, server: Server):
    """Coroutine for receiving and transmitting all messages"""

    # Update state
    server.clients.add(websocket)

    # Handle intro and update client
    raw_intro_msg = await websocket.recv()
    intro_msg = loads(raw_intro_msg)
    client_name = intro_msg[1]["client_name"]
    print(f"Client '{client_name}' Connecting...")
    
    init_message = server.handle_intro()
    await send(websocket, init_message)

    # Listen for method invocation and keep all clients informed
    async for message in websocket:

        # Decode and print raw message
        message = loads(message)
        print(f"Message from client: {message}")

        # Handle the method invocation
        response, reply = server.handle_invoke(message)

        # Send response to all clients, and method reply to client
        websockets.broadcast(server.clients, dumps(response))
        await send(websocket, reply)


async def main():
    """
    Main method for maintaining websocket connection
    """

    server = Server(starting_state)
    print(f"Server initialized with objects: {server.objects}")

    # Create partial to pass server to handler
    handler = functools.partial(
        handle_client,
        server = server
    )

    print("Starting up Server...")
    async with websockets.serve(handler, "", 50000):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())