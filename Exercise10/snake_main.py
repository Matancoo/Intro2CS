import argparse
import game_utils
from snake_game import SnakeGame
from game_display import GameDisplay


def main_loop(gd: GameDisplay, args: argparse.Namespace) -> None:
    # INIT OBJECTS
    game = SnakeGame(args)
    gd.show_score(0)
    # DRAW BOARD
    game.draw_board(gd)

    gd.end_round()
    game.end_round()

    # END OF ROUND 0
    while not game.is_over():
        # CHECK KEY CLICKS
        key_clicked = gd.get_key_clicked()
        game.read_key(key_clicked)
        # UPDATE OBJECTS
        game.update_objects()

        # DRAW BOARD
        if not game.debug:
            gd.show_score(game.snake_score)
        game.draw_board(gd)
        # WAIT FOR NEXT ROUND:
        game.end_round()
        gd.end_round()


if __name__ == "__main__":
    pass
