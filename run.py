# 24301020086  阿依波塔·赛力克别克

from othellolib import init_board, display_board, create_player, game, move_input, move_random,move_AI

def main():
    player1 = create_player('🐁  张峰', move_input)
    player2 = create_player('🐁  李伟', move_AI)
    game(player1=player1, player2=player2)


if __name__ == "__main__":
    main()