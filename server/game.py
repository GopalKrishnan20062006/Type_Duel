import json
import random
from words import generate_words
import asyncio

class Game:

    def __init__(self):
        self.players = []

    async def add_player(self, websocket):

        self.players.append(websocket)

        print(f"Players connected: {len(self.players)}")

        if len(self.players) == 1:

            await websocket.send(json.dumps({
                "type": "status",
                "message": "Waiting for another player..."
            }))

        elif len(self.players) == 2:

            await self.start_game()

    async def remove_player(self, websocket):

        if websocket in self.players:
            self.players.remove(websocket)

        for player in self.players:

            await player.send(json.dumps({
                "type": "status",
                "message": "Opponent disconnected."
            }))

    async def start_game(self):
        for i in [3, 2, 1]:

            message = json.dumps({
                "type": "countdown",
                "value": i
            })

            for player in self.players:
                await player.send(message)

            await asyncio.sleep(1)
        text = generate_words()
        message = json.dumps({
            "type": "start",
            "text": text
        })
        for player in self.players:
            await player.send(message)
