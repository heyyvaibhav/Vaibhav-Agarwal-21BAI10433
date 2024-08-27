import asyncio
import websockets
import json

class Game:
    def __init__(self):
        self.players = []
        self.board = [['' for _ in range(5)] for _ in range(5)]
        self.current_turn = 0
        self.game_over = False

    def add_player(self, websocket):
        if len(self.players) < 2:
            self.players.append(websocket)
            return True
        return False

    def setup_board(self, player_id, characters):
        for idx, char in enumerate(characters):
            if player_id == 0:
                self.board[0][idx] = f"A-{char}"
            else:
                self.board[4][idx] = f"B-{char}"

    def valid_move(self, player_id, char, move):
        # Implement the movement logic validation here based on the character and move
        return True

    def move_character(self, player_id, char, move):
        # Update the board state based on the move
        pass

    def check_game_over(self):
        # Implement game over check
        return False

    def get_game_state(self):
        return self.board

async def handle_client(websocket, path, game):
    player_id = len(game.players)
    if not game.add_player(websocket):
        await websocket.send(json.dumps({"type": "ERROR", "message": "Game is full"}))
        return

    await websocket.send(json.dumps({"type": "GAME_INIT", "player_id": player_id}))

    async for message in websocket:
        data = json.loads(message)
        if data['type'] == 'SETUP':
            game.setup_board(player_id, data['characters'])
            await websocket.send(json.dumps({"type": "STATE_UPDATE", "board": game.get_game_state()}))
        elif data['type'] == 'MOVE':
            char = data['char']
            move = data['move']
            if game.valid_move(player_id, char, move):
                game.move_character(player_id, char, move)
                if game.check_game_over():
                    game.game_over = True
                    await websocket.send(json.dumps({"type": "GAME_OVER", "winner": player_id}))
                else:
                    game.current_turn = 1 - game.current_turn
                    await websocket.send(json.dumps({"type": "STATE_UPDATE", "board": game.get_game_state()}))
            else:
                await websocket.send(json.dumps({"type": "INVALID_MOVE", "message": "Invalid move"}))

async def main():
    game = Game()
    async with websockets.serve(lambda ws, path: handle_client(ws, path, game), "localhost", 4000):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
