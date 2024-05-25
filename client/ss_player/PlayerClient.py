from __future__ import annotations
import asyncio
import websockets


class PlayerClient:
    def __init__(self, player_number: int, socket: websockets.WebSocketClientProtocol, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        self._socket = socket
        self._player_number = player_number
        self._player_char = 'o' if player_number == 1 else 'x'
        self._enemy_char = 'x' if player_number == 1 else 'o'
        self.trun = 0

    @property
    def player_number(self) -> int:
        return self._player_number

    async def close(self):
        await self._socket.close()

    async def play(self):
        while True:
            board = await self._socket.recv()
            action = self.create_action(board)
            await self._socket.send(action)
            if action == 'X000':
                raise SystemExit

    def create_action(self, board):
        actions = ''
        if self.turn == 0 and self.player_number == 1:
            return 'Q055'
        elif self.turn == 0 and self.player_number == 2:
            return 'Q2AA'
        else:
            # パスを選択
            return 'X000'

    @staticmethod
    async def create(url: str, loop: asyncio.AbstractEventLoop) -> PlayerClient:
        socket = await websockets.connect(url)
        print('PlayerClient: connected')
        player_number = await socket.recv()
        print(f'player_number: {player_number}')
        return PlayerClient(int(player_number), socket, loop)
