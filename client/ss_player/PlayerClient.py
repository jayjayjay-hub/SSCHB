from __future__ import annotations
import asyncio
import websockets

import numpy as np
from enum import Enum
from typing import Any

class BlockType(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'
    I = 'I'
    J = 'J'
    K = 'K'
    L = 'L'
    M = 'M'
    N = 'N'
    O = 'O'
    P = 'P'
    Q = 'Q'
    R = 'R'
    S = 'S'
    T = 'T'
    U = 'U'
    X = 'X'

    @property
    def block_map(self) -> np.ndarray[Any, np.dtype[int]]:
        if self == BlockType.A:
            return np.array([[1]])
        elif self == BlockType.B:
            return np.array([[1], [1]])
        elif self == BlockType.C:
            return np.array([[1], [1], [1]])
        elif self == BlockType.D:
            '''
            type D:
             ■ 
             ■ ■ 
            '''
            return np.array([[1, 0], [1, 1]])
        elif self == BlockType.E:
            '''
            type E:
             ■ 
             ■ 
             ■ 
             ■ 
            '''
            return np.array([[1], [1], [1], [1]])
        elif self == BlockType.F:
            '''
            type F:
               ■ 
               ■ 
             ■ ■ 
            '''
            return np.array([[0, 1], [0, 1], [1, 1]])
        elif self == BlockType.G:
            '''
            type G:
             ■ 
             ■ ■ 
             ■    
            '''
            return np.array([[1, 0], [1, 1], [1, 0]])
        elif self == BlockType.H:
            '''
            type H:
             ■ ■ 
             ■ ■ 
            '''
            return np.array([[1, 1], [1, 1]])
        elif self == BlockType.I:
            '''
            type I:
             ■ ■ 
               ■ ■ 
            '''
            return np.array([[1, 1, 0], [0, 1, 1]])
        elif self == BlockType.J:
            '''
            type J:
             ■ 
             ■ 
             ■ 
             ■ 
             ■ 
            '''
            return np.array([[1], [1], [1], [1], [1]])
        elif self == BlockType.K:
            '''
            type K:
               ■ 
               ■ 
               ■ 
             ■ ■ 
            '''
            return np.array([[0, 1], [0, 1], [0, 1], [1, 1]])
        elif self == BlockType.L:
            '''
            type L:
               ■ 
               ■ 
             ■ ■ 
             ■ 
            '''
            return np.array([[0, 1], [0, 1], [1, 1], [1, 0]])
        elif self == BlockType.M:
            '''
            type M:
               ■ 
             ■ ■ 
             ■ ■ 
            '''
            return np.array([[0, 1], [1, 1], [1, 1]])
        elif self == BlockType.N:
            '''
            type N:
             ■ ■ 
               ■ 
             ■ ■ 
            '''
            return np.array([[1, 1], [0, 1], [1, 1]])
        elif self == BlockType.O:
            '''
            type O:
             ■ 
             ■ ■ 
             ■ 
             ■ 
            '''
            return np.array([[1, 0], [1, 1], [1, 0], [1, 0]])
        elif self == BlockType.P:
            '''
            type P:
               ■ 
               ■ 
             ■ ■ ■ 
            '''
            return np.array([[0, 1, 0], [0, 1, 0], [1, 1, 1]])
        elif self == BlockType.Q:
            '''
            type Q:
             ■ 
             ■ 
             ■ ■ ■ 
            '''
            return np.array([[1, 0, 0], [1, 0, 0], [1, 1, 1]])
        elif self == BlockType.R:
            '''
            type R:
             ■ ■ 
               ■ ■ 
                 ■ 
            '''
            return np.array([[1, 1, 0], [0, 1, 1], [0, 0, 1]])
        elif self == BlockType.S:
            '''
            type S:
             ■ 
             ■ ■ ■ 
                 ■ 
            '''
            return np.array([[1, 0, 0], [1, 1, 1], [0, 0, 1]])
        elif self == BlockType.T:
            '''
            type T:
             ■ 
             ■ ■ ■ 
               ■ 
            '''
            return np.array([[1, 0, 0], [1, 1, 1], [0, 1, 0]])
        elif self == BlockType.U:
            '''
            type U:
               ■ 
             ■ ■ ■ 
               ■ 
            '''
            return np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        elif self == BlockType.X:
            '''
            type X:パスをする時用
                 
                   
                 
            '''
            return np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        
        else:
            raise NotImplementedError

class PlayerClient:
    def __init__(self, player_number: int, socket: websockets.WebSocketClientProtocol, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        self._socket = socket
        self._player_number = player_number
        self._player_char = 'o' if player_number == 1 else 'x'
        self._enemy_char = 'x' if player_number == 1 else 'o'
        self._block_types = [chr(i) for i in range(65, 86)] + ['X']
        self.coordinate_map = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E'}
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
        # ボードの状態を2次元配列に変換
        board = '0' + board.lstrip('\n')
        board_lines = board.strip().split('\n')[1:]  # インデックス行をスキップ
        board_array = np.array([list(line[1:]) for line in board_lines])  # インデックス列をスキップ
        # board_array index 0-13 x 0-13

        # 最初のターンなら
        if self.trun == 0:
            actions = self.first_turn(board_array, self._player_char)
        # 2ターン目以降なら
        else:
            actions = self.serch_best_action(board_array, self._player_char)
        self.trun += 1
        return actions

    def first_turn(self, board_array, player_char):
        if player_char == 'o':
            block_type = self._block_types.pop(self._block_types.index('Q'))
            return block_type + '055'
        if player_char == 'x':
            block_type = self._block_types.pop(self._block_types.index('Q'))
            return block_type + '488'

    def serch_best_action(self, board_array, player_char):
        block_type = self._block_types.pop(0)
        x, y = self.serch_coordinate(board_array, block_type, player_char) # tuple (int, int)
        if x == -1:
            return 'X000'
        char_x = self.coordinate_map[x + 1]
        char_y = self.coordinate_map[y + 1]

        return block_type + '0' + char_x + char_y

    def serch_coordinate(self, board_array, block_type, player_char):
        # board_array 14x14 numpy array (index 0-13 x 0-13)
        block = BlockType(block_type).block_map # numpy array

        board_height, board_width = board_array.shape # (14, 14)
        block_height, block_width = block.shape # (3, 3)

        for i in range(board_height - block_height + 1): # if block_height = 3, range(12)
            for j in range(board_width - block_width + 1):
                if self.is_legal_move(board_array, block, i, j, player_char):
                    return i, j
        return -1, -1

    def is_legal_move(self, board_array, block, x, y, player_char):
        board_height, board_width = board_array.shape # (14, 14)
        block_height, block_width = block.shape
        touch_the_corner = False

        for i in range(block_height):
            for j in range(block_width):
                if block[i, j] == 1:
                    # ボードの範囲外かどうか
                    # if x + i >= board_height or y + j >= board_width:
                    #     return False

                    # 空いているマスかどうか
                    if board_array[x + i, y + j] != '.':
                        return False

                    # 自分の他のブロックの角と接しているか
                    if not touch_the_corner:
                        touch_the_corner = self.check_touch_the_corner(board_array, x, y, player_char)

                    # 他のブロックの辺に接しているか
                    if self.check_touch_the_edge(board_array, x, y, player_char):
                        return False
        if not touch_the_corner:
            return False
        return True

    def check_touch_the_corner(self, board_array, x, y, player_char):
        # board_array 14x14 numpy array (index 0-13 x 0-13)
        if (x > 0 and y > 0) and board_array[x - 1, y - 1] == player_char:
            return True
        if (x > 0 and y < 13) and board_array[x - 1, y + 1] == player_char:
            return True
        if (x < 13 and y > 0) and board_array[x + 1, y - 1] == player_char:
            return True
        if (x < 13 and y < 13) and board_array[x + 1, y + 1] == player_char:
            return True
        return False
    
    def check_touch_the_edge(self, board_array, x, y, player_char):
        # board_array 14x14 numpy array (index 0-13 x 0-13)
        if x > 0 and board_array[x - 1, y] == player_char:
            return True
        if x < 13 and board_array[x + 1, y] == player_char:
            return True
        if y > 0 and board_array[x, y - 1] == player_char:
            return True
        if y < 13 and board_array[x, y + 1] == player_char:
            return True
        return False


    @staticmethod
    async def create(url: str, loop: asyncio.AbstractEventLoop) -> PlayerClient:
        socket = await websockets.connect(url)
        print('PlayerClient: connected')
        player_number = await socket.recv()
        print(f'player_number: {player_number}')
        return PlayerClient(int(player_number), socket, loop)
