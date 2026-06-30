import json
import random
from words import generate_words

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

    async def start_game(self):

        text = generate_words()

        message = json.dumps({

            "type": "start",

            "text": text

    })

        for player in self.players:
            await player.send(message)
