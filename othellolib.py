"""
Python程序设计 期末大作业——翻转棋
24301020086  阿依波塔·赛力克别克
"""

import time
import sys
import random

# 棋盘状态：黑棋, 白棋, 空棋
BLACK, WHITE, EMPTY = -1, 1, 0

direction = [
    (-1, -1), (-1, 0), (-1, 1),  # NW, N, NE
    (0, -1),         (0, 1),     # W, E
    (1, -1), (1, 0), (1, 1)      # SW, S, SE
] #八个方向矩阵

if "idlelib" in sys.modules:
    BLACK_PIECE = " ● "
    WHITE_PIECE = " ○ "
    EMPTY_PIECE = " □ "
    END_ROW = " "
else:
    # 使用Emoji表示棋盘， BG_EMPTY设置背景色为绿色， BG_RESET是重置背景色
    BG_EMPTY, BG_RESET = "\x1b[42m", "\x1b[0m"
    BLACK_PIECE = f"{BG_EMPTY}⚫️{BG_RESET}"
    EMPTY_PIECE = f"{BG_EMPTY}🟩{BG_RESET}"
    WHITE_PIECE = f"{BG_EMPTY}⚪️{BG_RESET}"
    END_ROW = f"{BG_EMPTY} {BG_RESET}"

def stone(piece):
    """
    棋子的Emoji显示
    参数: 棋子类型(piece): -1, 0, 1, 对应黑棋、空棋、白棋
    """
    stone_coes = [
        BLACK_PIECE,
        EMPTY_PIECE,
        WHITE_PIECE,
    ]
    return stone_coes[piece + 1]

def init_board(n=8):
    """
    创建棋盘并设置初始的4枚棋子
    参数: 棋盘规格(n)
    """
    board = [[0 for _ in range(n)] for _ in range(n)]

    C0, C1 = n // 2, n // 2 - 1
    board[C0][C0], board[C1][C1] = WHITE, WHITE  # White
    board[C1][C0], board[C0][C1] = BLACK, BLACK  # Black

    return board

def display_board(board, sleep=0):
    """
    显示棋盘状态
    参数: 棋盘(board), 暂停时间(sleep)
    """
    n = len(board)
    print("    " + " ".join([chr(65 + i) for i in range(n)]))  # 打印列标签 A-H
    for i, row in enumerate(board):
        print(f"{chr(65 + i)}  ", end="")  # 打印行标签 A-H
        for piece in row:
            print(stone(piece), end="")
        print(END_ROW, end="")
        print()  # New line after each row
    if sleep > 0:
        time.sleep(sleep)

def is_valid_move(board, row, col, piece):
    """
    检查落子是否合法。
    """
    if board[row][col] != EMPTY:
        return False
    opponent = BLACK if piece == WHITE else WHITE
    for drow, dcol in direction:
        r, c = row + drow, col + dcol
        has_opponent = False
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opponent:
            has_opponent = True
            r += drow
            c += dcol
        if has_opponent and 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == piece:
            return True
    return False

def get_valid_moves(board, piece):
    """
    获取所有合法的落子位置。
    """
    valid_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_valid_move(board, row, col, piece):
                valid_moves.append((row, col))
    return valid_moves

def do_move(board, row, col, piece):
    """
    执行落子操作并翻转棋子。
    """
    board[row][col] = piece
    opponent = BLACK if piece == WHITE else WHITE
    for drow, dcol in direction:
        r, c = row + drow, col + dcol
        path = []
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opponent:
            path.append((r, c))
            r += drow
            c += dcol
        if path and 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == piece:
            for pr, pc in path:
                board[pr][pc] = piece

def move_input(board, piece, name):
    """
    返回玩家下一手的位置(row, col)。
    参数: 棋盘(board), 棋子类型(piece), 玩家名称(name)
    """
    while True:
        valid_moves = get_valid_moves(board, piece)
        if not valid_moves:
            print(f"No valid moves for {name}.")
            return None, None
        move = input(f"{name}, enter your move (e.g., A B) or '?' to see valid moves: ").strip()
        if move == '?':
            print(f"Valid moves for {name}: {[f'{chr(65 + r)} {chr(65 + c)}' for r, c in valid_moves]}")
            continue
        try:
            row, col = move.split()
            row, col = ord(row.upper()) - 65, ord(col.upper()) - 65
            if (row, col) in valid_moves:
                return row, col
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter row and column separated by a space.")

def move_random(board, piece, name):
    """
    随机选择一个合法的落子位置。
    """
    valid_moves = get_valid_moves(board, piece)
    if valid_moves:
        return random.choice(valid_moves)
    else:
        return None, None
    
def move_AI(board, piece, name):
    """
    AI选择最合适的落子位置
    机制为： 1. 当所有合法落子位置都不在边上(第A, H行或列)或者角上(AA, HH, AH, HA)时，选择落子后能翻转的棋子最多的点，如果有多个相同的则在其中随机选择一个
            2. 当存在合法落子位置在边上(第A, H行或列)或者角上(AA, HH, AH, HA)时，选择在边上/角上的点，角点的优先级高于边点，如存在多个符合要求的则选择能翻转棋子最多的点
    """
    valid_moves = get_valid_moves(board, piece)
    if not valid_moves:
        return None, None
    
    corners = [(0, 0), (0, len(board) - 1), (len(board) - 1, 0), (len(board) - 1, len(board) - 1)]
    edges = [(r, c) for r in range(len(board)) for c in range(len(board)) if r == 0 or r == len(board) - 1 or c == 0 or c == len(board) - 1]

    # 检查角点
    corner_moves = [move for move in valid_moves if move in corners]
    if corner_moves:
        return max(corner_moves, key=lambda move: count_flipped_pieces(board, move[0], move[1], piece))

    # 检查边点
    edge_moves = [move for move in valid_moves if move in edges]
    if edge_moves:
        return max(edge_moves, key=lambda move: count_flipped_pieces(board, move[0], move[1], piece))

    # 选择翻转棋子最多的位置
    return max(valid_moves, key=lambda move: count_flipped_pieces(board, move[0], move[1], piece))

def count_flipped_pieces(board, row, col, piece):
    """
    计算在指定位置落子后可以翻转的棋子数量。
    """
    opponent = BLACK if piece == WHITE else WHITE
    count = 0
    for drow, dcol in direction:
        r, c = row + drow, col + dcol
        path_count = 0
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opponent:
            path_count += 1
            r += drow
            c += dcol
        if path_count > 0 and 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == piece:
            count += path_count
    return count

def move_one_step(player, board):
    """
    玩家在棋盘上走一步。
    参数：玩家和棋盘
    """
    name, piece, move = player['name'], player['piece'], player['move']
    print(f"{name}'s turn ({'Black' if piece == BLACK else 'White'}).")
    row, col = move(board, piece, name)
    if row is None or col is None:
        print(f"{name} has no valid moves. Skipping turn.")
        return "SKIP"

    if is_valid_move(board, row, col, piece):
        do_move(board, row, col, piece)
        display_board(board)
        return "CONTINUE"
    else:
        print("Invalid move. Try again.")
        return "WRONG"

def game(player1, player2, n=8):
    """
    游戏入口函数。
    参数: 两个玩家, 其中player1执黑, player2执白.
    """
    player1["piece"] = BLACK  # 黑棋
    player2["piece"] = WHITE  # 白棋

    board = init_board(n)
    display_board(board)
    players = [player1, player2]
    turn = 0

    while True:
        status = move_one_step(players[turn], board)
        if status == "SKIP":
            if move_one_step(players[1 - turn], board) == "SKIP":
                break
        elif status == "WRONG":
            continue
        turn = 1 - turn

        if not any(is_valid_move(board, r, c, players[turn]["piece"]) for r in range(n) for c in range(n)):
            print("No valid moves left. Game Over!")
            break
        
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)

    if black_count > white_count:
        print(f"Game Over\n{player1['name']}(Black) Win!")
    elif white_count > black_count:
        print(f"Game Over\n{player2['name']}(White) Win!")
    else:
        print("Game Over\nIt's a Draw!")

    print(f"{player1['name']}(Black) : {player2['name']}(White) = {black_count}:{white_count}")

def create_player(name, move):
    """
    创建玩家
    参数: 玩家名称(name), 玩家使用的选择下一步位置的函数(move)
    """
    return {
        "name": name,
        "move": move,
        "piece": None,
    }

def test_board():
    board = init_board()
    display_board(board)

if __name__ == "__main__":
    test_board()