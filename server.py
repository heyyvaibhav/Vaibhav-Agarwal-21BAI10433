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
        player_prefix = 'A-' if player_id == 0 else 'B-'
        # Find the character's current position
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == player_prefix + char:
                    current_pos = (i, j)
                    break
        else:
            return False  # Character not found

        x, y = current_pos
        dx, dy = 0, 0

        if move == 'L': dy = -1
        elif move == 'R': dy = 1
        elif move == 'F': dx = -1 if player_id == 0 else 1
        elif move == 'B': dx = 1 if player_id == 0 else -1
        elif move == 'FL': dx, dy = (-1 if player_id == 0 else 1), -1
        elif move == 'FR': dx, dy = (-1 if player_id == 0 else 1), 1
        elif move == 'BL': dx, dy = (1 if player_id == 0 else -1), -1
        elif move == 'BR': dx, dy = (1 if player_id == 0 else -1), 1
        else: return False

        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 5 and 0 <= new_y < 5:
            if self.board[new_x][new_y] == '' or self.board[new_x][new_y][0] != player_prefix[0]:
                return True
        return False

    def move_character(self, player_id, char, move):
        player_prefix = 'A-' if player_id == 0 else 'B-'
        # Find the character's current position
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == player_prefix + char:
                    current_pos = (i, j)
                    break

        x, y = current_pos
        dx, dy = 0, 0

        if move == 'L': dy = -1
        elif move == 'R': dy = 1
        elif move == 'F': dx = -1 if player_id == 0 else 1
        elif move == 'B': dx = 1 if player_id == 0 else -1
        elif move == 'FL': dx, dy = (-1 if player_id == 0 else 1), -1
        elif move == 'FR': dx, dy = (-1 if player_id == 0 else 1), 1
        elif move == 'BL': dx, dy = (1 if player_id == 0 else -1), -1
        elif move == 'BR': dx, dy = (1 if player_id == 0 else -1), 1

        new_x, new_y = x + dx, y + dy
        if self.valid_move(player_id, char, move):
            self.board[new_x][new_y] = player_prefix + char
            self.board[x][y] = ''

    def check_game_over(self):
        # Check if either player has no remaining characters
        player_a_has_chars = any('A-' in cell for row in self.board for cell in row)
        player_b_has_chars = any('B-' in cell for row in self.board for cell in row)

        if not player_a_has_chars or not player_b_has_chars:
            return True
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
    async with websockets.serve(lambda ws, path: handle_client(ws, path, game), "localhost", 6789):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
