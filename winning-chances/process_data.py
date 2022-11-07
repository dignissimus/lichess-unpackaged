import json
import sys

import chess.pgn

NGAMES = 1000


def valid(game):
    white_elo = int(game.headers["WhiteElo"])
    black_elo = int(game.headers["BlackElo"])
    time_control = game.headers["TimeControl"]

    if time_control == "-":
        return False

    limit, increment = time_control.split("+")
    estimated_time = int(limit) + 40 * int(increment)

    high_rated = (white_elo + black_elo) / 2 > 1800
    is_rapid = 480 <= estimated_time < 1500
    has_analysis = game.next() and game.next().eval() is not None

    return has_analysis and high_rated and is_rapid


def main():
    positions = []
    with open("data/games.pgn", "w") as file:
        for i in range(NGAMES):
            game = chess.pgn.read_game(sys.stdin)
            while not valid(game):
                game = chess.pgn.read_game(sys.stdin)

            result = game.headers["Result"]
            match result:
                case "1-0":
                    score = 1
                case "0-1":
                    score = -1
                case "1/2-1/2":
                    score = 0
            while not game.is_end():
                game = game.next()
                evaluation = game.eval()
                if evaluation is not None:
                    positions.append((evaluation.white().score(mate_score=128), score))

            print(game, end="\n\n", file=file)
            print(i / 10)

    with open("data/positions.json", "w") as file:
        json.dump(positions, file)


if __name__ == "__main__":
    main()
