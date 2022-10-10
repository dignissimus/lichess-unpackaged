import itertools

import chess
import chess.engine
import chess.pgn
import numpy as np

WINDOW_SIZE = 6
STARTING_POSITION_EVALUATION = chess.engine.Cp(0)
SELECTORS = {
    chess.WHITE: lambda: itertools.cycle([True, False]),
    chess.BLACK: lambda: itertools.cycle([False, True]),
}


def winning_chance(cp):
    mul = -0.00368208
    val = 2 / (1 + np.exp(mul * cp)) - 1
    return 0.5 + np.maximum(-1, np.minimum(val, 1)) / 2


def move_accuracy(delta):
    return (103.1668 * np.exp(-0.04354 * 100 * delta) - 3.1669) / 100


def main():
    with open("long-game.pgn") as file:
        game = chess.pgn.read_game(file)

    mainline = game.mainline()
    evals = {colour: [] for colour in chess.COLORS}

    evaluations = [node.parent.eval() for node in mainline]
    evaluations[0] = chess.engine.PovScore(STARTING_POSITION_EVALUATION, chess.WHITE)
    evaluations = np.array(
        [evaluation.white().score(mate_score=100000) for evaluation in evaluations]
    )

    chances = winning_chance(evaluations)

    # Calculate the deltas by multiplying the differences in winning chances by by 1 and -1
    #  to account for both white and black
    deltas = np.diff(chances) * np.array(
        list(itertools.islice(itertools.cycle([-1, 1]), len(evaluations) - 1))
    )
    accuracies = move_accuracy(deltas)

    # Generate the windows, if there aren't enough moves to create a full window,
    #  a truncated window is created with all the moves available
    windows = [
        chances[max(0, index - WINDOW_SIZE + 1): index + 1]
        for index in range(len(chances) - 1)
    ]

    # The weight is the standard deviation and is calculated for every window
    # Here, the standard deviation represents evaluation volatility
    weights = np.array([np.std(window) for window in windows])
    weighted_accuracies = accuracies * weights

    # Select the move accuracies relevant for each player
    accuracies_and_weights = {
        colour: (
            list(itertools.compress(accuracies, selector())),
            list(itertools.compress(weights, selector())),
        )
        for colour, selector in SELECTORS.items()
    }

    print("Evaluation\tWeight")
    for evaluation, weight in zip(evaluations, weights):
        print(np.round(evaluation / 100, 2), int(weight * 100), sep="\t\t")

    print()
    for colour, (m_accuracies, m_weights) in accuracies_and_weights.items():
        accuracy = np.dot(m_accuracies, m_weights) / np.sum(m_weights)
        print(chess.COLOR_NAMES[colour], accuracy * 100)


if __name__ == "__main__":
    main()
