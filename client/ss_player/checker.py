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
            ''' 
            type A:
             ■ 
            '''
            return np.array([[1]])
        elif self == BlockType.B:
            ''' 
            type B:
             ■ 
             ■ 
            '''
            return np.array([[1], [1]])
        elif self == BlockType.C:
            '''
            type C:
             ■ 
             ■ 
             ■ 
            '''
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

def is_legal_move(board: str, block: np.array, x: int, y: int, player: int) -> bool:
    """
    ボード上にブロックを合法的に配置できるかどうかをチェックする関数。

    :param board: ボードの状態を表す文字列
    :param block: 配置するブロックの形状を表す2次元numpy配列
    :param x: 配置するブロックの左上のx座標（1から始まる）
    :param y: 配置するブロックの左上のy座標（1から始まる）
    :param player: プレイヤー番号（1なら'o', 2なら'x'）
    :return: 配置が合法ならTrue、そうでなければFalse
    """
    # ボードを解析して2次元numpy配列に変換
    # board_lines = board.strip().split('\n')[1:]  # インデックス行をスキップ
    # board_array = np.array([list(line[1:]) for line in board_lines])  # インデックス列をスキップ
    board = '0' + board
    board_lines = board.strip().split('\n')[:]
    board_array = np.array([list(line) for line in board_lines])
    print(board_array)

    board_height, board_width = board_array.shape
    block_height, block_width = block.shape
    player_char = 'o' if player == 1 else 'x'
    _block_types = [chr(i) for i in range(65, 86)] + ['X']
    block_type = _block_types.pop(_block_types.index('Q'))
    print(block_type)

    coordinate_map = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E'}

    # ボードの境界チェック
    if x - 1 + block_width > board_width or y - 1 + block_height > board_height:
        return False

    # ブロックが他のブロックと接触するかどうかを記録する変数
    corner_contact = False

    for i in range(block_height):
        for j in range(block_width):
            if block[i, j] == 1:
                board_x, board_y = x - 1 + j, y - 1 + i

                # 他のブロックとの重なりをチェック
                if board_array[board_y, board_x] != '.':
                    return False

                # ブロックの角が他のブロックの角に接触しているかチェック
                for dy, dx in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    ny, nx = board_y + dy, board_x + dx
                    if 0 <= nx < board_width and 0 <= ny < board_height and board_array[ny, nx] == player_char:
                        corner_contact = True

                # ブロックの辺が他のブロックの辺と接触していないことをチェック
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ny, nx = board_y + dy, board_x + dx
                    if 0 <= nx < board_width and 0 <= ny < board_height and board_array[ny, nx] == player_char:
                        return False

    return corner_contact

# 使用例
if __name__ == "__main__":
    board_str = """
123456789ABCDE
1.o..ooo.oooo..
2.ooo.o......o.
3o.o....o.oo.oo
4o..o.oooo.oo.o
5o.ooo....xxo.o
6oo.o.ooooox.o.
7.xo..xxx.xx.o.
8.xo.....x..oo.
9.x.oxxx.x.xxxx
A.x.oo.xx.x....
B.x.oox....xxxx
C..xxxx.x....x.
D......xxx.xx..
E.......x.xxx..
"""
    board = '0' + board_str.lstrip('\n')
    board_lines = board.strip().split('\n')
    board_array = np.array([list(line) for line in board_lines])
    print(board_array)

    block_A = BlockType.A.block_map
    # 配置の例
    x, y = 6, 14  # 座標 (x, y)
    player = 2  # 'x'プレイヤー

    # 配置が合法かどうかチェック
    is_legal = is_legal_move(board_str, block_A, x, y, player)
    print("配置が合法かどうか:", is_legal)
