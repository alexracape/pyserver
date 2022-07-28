import asyncio
import functools

import websockets
from cbor2 import loads, dumps

from pyserver.core import Server
from pyserver.noodle_objects import Component

async def send(websocket, message: list):
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
        reply = server.handle_invoke(message[1])
        print(f"Reply: {reply}")

        # Send method reply to client
        await send(websocket, reply)

    # Remove client if disconnected
    print(f"Client 'client_name' disconnected")
    server.clients.remove(websocket)


async def start_server(port: int, methods: dict, starting_state: dict, delegates: dict[Component, object]=None):
    """
    Main method for maintaining websocket connection
    """

    server = Server(methods, starting_state, delegates)
    Component.host_server = server
    print(f"Server initialized with objects: {server.objects}")

    # Create partial to pass server to handler
    handler = functools.partial(
        handle_client,
        server = server
    )

    print("Starting up Server...")
    async with websockets.serve(handler, "", port):
        await asyncio.Future()  # run forever
