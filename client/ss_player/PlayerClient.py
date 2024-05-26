from __future__ import annotations
import asyncio
import websockets

import numpy as np

# import random

from ss_player.BlockType import BlockType


class PlayerClient:

    FREE_SPACE = 2
    SIDE_ENEMY = 1
    PRE_VERTEX_PLAYER = 3
    VERTEX_PLAYER = -1
    VERTEX_ENEMY = 5
    DISABLE = 9

    DEPTH = 3
    BREADTH = 10

    def __init__(self, player_number: int, socket: websockets.WebSocketClientProtocol, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        self._socket = socket
        self._player_number = player_number
        self._player_char = 'o' if player_number == 1 else 'x'
        self._enemy_char = 'x' if player_number == 1 else 'o'
        self._block_types = [chr(i) for i in range(65, 86)] + ['X']
        self.coordinate_map = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E'}
        self.tmp_board = None
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
        board_lines = board.strip().split('\n')[1:]  # インデックス行をスキップ
        board_array = np.array([list(line[1:]) for line in board_lines])  # インデックス列をスキップ
        # board_array index 0-13 x 0-13

        # 最初のターンなら
        if self.trun == 0:
            actions = self.first_turn(board_array, self._player_char)
            self.trun += 1
            return actions

        cp_board = self.init_board(board_array, self._player_char)
        # print(cp_board)
        # print('\n')
        # print(self.tmp_board)
        # 2ターン目以降なら
        actions = self.serch_best_action(cp_board)
        self.trun += 1
        return actions

    def init_board(self, board_array, player_char):
        expansion_board = board_array.copy()
        expansion_board = np.insert(expansion_board, 0, '9', axis=0)
        expansion_board = np.insert(expansion_board, 0, '9', axis=1)
        expansion_board = np.insert(expansion_board, expansion_board.shape[0], '9', axis=0)
        expansion_board = np.insert(expansion_board, expansion_board.shape[1], '9', axis=1)
        cp_board = np.zeros(expansion_board.shape, dtype=np.int8)
        self.tmp_board = np.zeros(expansion_board.shape, dtype=np.int8)
        for i in range(expansion_board.shape[0]):
            for j in range(expansion_board.shape[1]):
                if expansion_board[i, j] == '9':
                    cp_board[i, j] = self.DISABLE
                elif expansion_board[i, j] == player_char:
                    self.write_corner(cp_board, i, j)
                elif expansion_board[i, j] == self._enemy_char:
                    self.write_enemy(cp_board, i, j)

        for i in range(cp_board.shape[0]):
            for j in range(cp_board.shape[1]):
                if cp_board[i, j] == self.PRE_VERTEX_PLAYER:
                    self.tmp_board[i, j] = True
                    cp_board[i, j] = self.VERTEX_PLAYER
                elif cp_board[i, j] == 0:
                    cp_board[i, j] = self.FREE_SPACE

        return cp_board

    def write_corner(self, cp_board, x, y):
        array = [[self.PRE_VERTEX_PLAYER, self.DISABLE, self.PRE_VERTEX_PLAYER],
                 [self.DISABLE, self.DISABLE, self.DISABLE],
                 [self.PRE_VERTEX_PLAYER, self.DISABLE, self.PRE_VERTEX_PLAYER]]
        for i in range(3):
            for j in range(3):
                if self.priority(cp_board[x + i - 1, y + j - 1], array[i][j]):
                    cp_board[x + i - 1, y + j - 1] = array[i][j]

    def write_enemy(self, cp_board, x, y):
        array = [[self.VERTEX_ENEMY, self.SIDE_ENEMY, self.VERTEX_ENEMY],
                 [self.SIDE_ENEMY, self.DISABLE, self.SIDE_ENEMY],
                 [self.VERTEX_ENEMY, self.SIDE_ENEMY, self.VERTEX_ENEMY]]
        for i in range(3):
            for j in range(3):
                if self.priority(cp_board[x + i - 1, y + j - 1], array[i][j]):
                    if cp_board[x + i - 1, y + j - 1] == self.PRE_VERTEX_PLAYER and array[i][j] == self.VERTEX_ENEMY:
                        self.tmp_board[x + i - 1, y + j - 1] = True
                    cp_board[x + i - 1, y + j - 1] = array[i][j]

    def priority(self, dst, src):
        if dst == self.SIDE_ENEMY and src == self.VERTEX_ENEMY:
            return False
        if dst == self.VERTEX_ENEMY and src == self.SIDE_ENEMY:
            return True
        return dst < src

    def first_turn(self, board_array, player_char):
        if player_char == 'o':
            block_type = self._block_types.pop(self._block_types.index('R'))
            return block_type + '055'
        if player_char == 'x':
            block_type = self._block_types.pop(self._block_types.index('R'))
            return block_type + '488'

    def serch_best_action(self, cp_board):
        best = -100
        best_action = ''
        # reverse _block_types
        for block_type in self._block_types[::-1]:
            for rote in range(8):
                for x in range(1, cp_board.shape[0] - 1):
                    for y in range(1, cp_board.shape[1] - 1):
                        if self.check_in_corner(cp_board, BlockType(block_type).block_map, x, y):
                            prio = self.calc_prio(cp_board, BlockType(block_type).block_map, x, y)
                            if prio > best:
                                best = prio
                                best_action = block_type + str(rote) + self.coordinate_map[x] + self.coordinate_map[y]

        if best_action == '':
            return 'X000'
        self._block_types.pop(self._block_types.index(best_action[0]))
        return best_action

    def calc_prio(self, cp_board, block, x, y) -> int:
        prio = 0
        for i in range(block.shape[0]):
            for j in range(block.shape[1]):
                if block[i, j] == 1:
                    prio += cp_board[y + i, x + j]
        return prio

    def check_in_corner(self, cp_board, block, x, y):
        ans = False
        for i in range(block.shape[0]):
            for j in range(block.shape[1]):
                if block[i, j] == 1 and cp_board[y + i, x + j] == self.DISABLE:
                    return False
                if block[i, j] == 1 and self.tmp_board[y + i, x + j]:
                    ans = True
        return ans

    # def serch_best_action(self, board_array, player_char, serch_count=0):
    #     length = len(self._block_types)
    #     # random choice block_type get not pop
    #     block_type = self._block_types[random.randint(0, length - 1)]
    #     rote, x, y = self.serch_coordinate(board_array, block_type, player_char) # tuple (int, int)
    #     # x, y = self.serch_coordinate(board_array, block_type, player_char) # tuple (int, int)
    #     if x >= 0:
    #         # remove block_type
    #         self._block_types.pop(self._block_types.index(block_type))
    #         # int -> str rote
    #         str_rote = str(rote)
    #         char_x = self.coordinate_map[x + 1]
    #         char_y = self.coordinate_map[y + 1]
    #         return block_type + str_rote + char_x + char_y
    #         # return block_type + '0' + char_x + char_y
    #     elif serch_count < 10:
    #         # one more chance
    #         return self.serch_best_action(board_array, player_char, serch_count + 1)
    #     else:
    #         return 'X000'

    def serch_coordinate(self, board_array, block_type, player_char):
        # board_array 14x14 numpy array (index 0-13 x 0-13)
        block = BlockType(block_type).block_map # numpy array

        board_height, board_width = board_array.shape # (14, 14)
        block_height, block_width = block.shape

        for i in range(board_height - block_height + 1): # if block_height = 3, range(12)
            for j in range(board_width - block_width + 1):
                for k in range(8):
                    tmp_block = BlockType.rotate_and_flip(block, k)
                    if self.is_legal_move(board_array, tmp_block, j, i, player_char):
                        return k, i, j
        return -1, -1, -1

    def is_legal_move(self, board_array, block, x, y, player_char):
        board_height, board_width = board_array.shape # (14, 14)
        block_height, block_width = block.shape
        touch_the_corner = False

        for i in range(block_height):
            for j in range(block_width):
                if block[i, j] == 1:
                    # ボードの範囲外かどうか
                    if x + i >= board_height or y + j >= board_width:
                        return False

                    # 空いているマスかどうか
                    if board_array[x + i, y + j] != '.':
                        return False

                    # 自分の他のブロックの角と接しているか
                    if not touch_the_corner:
                        touch_the_corner = self.check_touch_the_corner(board_array, x + i, y + j, player_char)

                    # 他のブロックの辺に接しているか)
                    if self.check_touch_the_edge(board_array, x + i, y + j, player_char):
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
