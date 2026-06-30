import asyncio
from pathlib import Path
import json
import websockets
from aiohttp import web
from game import Game

CLIENT_FOLDER = Path(__file__).parent.parent / "client"

game = Game()

async def websocket_handler(websocket):
    print("Client connected")

    try:
        async for message in websocket:
            data = json.loads(message)
            print("Received:", data)

            if data["type"] == "join":
                await game.add_player(websocket)

            elif data["type"] == "progress":
                pass

            elif data["type"] == "finished":
                print(data)

    except websockets.ConnectionClosed:
        print("Client disconnected")

    finally:
        await game.remove_player(websocket)
        print("Player removed")

async def start_websocket():
    server = await websockets.serve(
        websocket_handler,
        "localhost",
        8765
    )

    print("WebSocket running on ws://localhost:8765")

    return server


async def start_http():
    app = web.Application()

    app.router.add_get(
        "/",
        lambda request: web.FileResponse(CLIENT_FOLDER / "index.html")
    )

    app.router.add_static("/", CLIENT_FOLDER)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "localhost", 8000)
    await site.start()

    print("Website running at http://localhost:8000")


async def main():
    ws_server = await start_websocket()
    await start_http()

    await ws_server.wait_closed()


asyncio.run(main())