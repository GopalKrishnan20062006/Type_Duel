import asyncio
import websockets

async def main():
    async with websockets.connect("ws://localhost:8765") as websocket:
        print("Connected")
        await websocket.send("Hello server")
        await asyncio.sleep(5)
asyncio.run(main())