import json
import random

import chess.pgn
import jax
import jax.numpy as jnp
import numpy as np
import scipy.optimize
from matplotlib import pyplot as plt


def tan_model(x, k1, k2):
    """
    Referring to a generic lc0 model
    """
    return np.arctan(x / k1) / k2


def current_lichess_model(x):
    """
    The current model used on Lichess
    """
    return 2 / (1 + np.exp(-0.003682081729595926 * x)) - 1


def filter_out_draws(xs, ys):
    # Remove games with draw scores
    return zip(*[(x, y) for (x, y) in zip(xs, ys) if y != 0])


def prepare_data(xs, ys, seed=None, size=None):
    # Deterministically shuffle the data for reproducibility
    if seed:
        random.seed(seed)
        xs, ys = zip(*random.sample(list(zip(xs, ys)), len(xs)))

    # Exclude draws when calculating loss
    xs, ys = filter_out_draws(xs, ys)

    # Convert data into jax-numpy arrays
    xs = jnp.array([float(x) for x in xs])
    ys = jnp.array([y for y in ys])

    # Limit the size of the data to be processed if specified
    if size:
        return xs[:size], ys[:size]

    return xs, ys


def build_logistic_model(xs, ys):
    def logistic_sigmoid(x):
        return 1 / (1 + jnp.exp(x))

    def loss(b, w):
        # Using binary crossentropy as the loss function

        # ys represents the expected score for white
        # The expected score sits in the range [-1, 1]
        expected_score = ys

        # Convert the expected score to a category [0, 1]
        # 0 represents a black win, 1 represents a white win
        category = (expected_score + 1.0) / 2.0

        # Calculate the predicted category probabilities
        predicted_category = logistic_sigmoid(b + w * xs / 100)

        # Binary crossentropy is undefined for p = 0, p = 1
        # So select epsilon to ensure values are not close to 0 or 1
        epsilon = 1e-5

        # Cross entropy loss
        crossentropy_loss = -jnp.mean(
            category * jnp.log(predicted_category + epsilon)
            + (1.0 - category) * jnp.log(1 - predicted_category - epsilon)
        )

        # L2 regularisation
        regularisation_term = 0.005 * w**2

        return crossentropy_loss + regularisation_term

    # Finding optimal b, w in the model sigmoid(b + wx)
    b = 0.0
    w = 0.0

    # Choose a learning rate
    learning_rate = 0.001

    # Use jax to calcualte the derivative of the loss function
    loss_gradient = jax.grad(loss, argnums=(0, 1))

    for i in range(100_000):
        db, dw = loss_gradient(b, w)
        if db + dw < 1e-3:
            break
        w -= learning_rate * dw
        b -= learning_rate * db

    print(f"b = {b}, w = {w}")
    print(f"f(x) = 1 / (1 + e^({b} + {w / 100} * x))")
    print("f(x) between 0 and 1")
    print("x is in centipawns")

    def trained_model(x):
        # The model, on its own, returns category probabilities
        # Shift it so that it returns an expected score
        return 2 * logistic_sigmoid(b + w * x / 100) - 1

    return trained_model


def main():
    positions = []
    with open("data/positions.json") as file:
        positions = json.load(file)
        xs, ys = zip(*positions)

    linspace = np.linspace(min(xs), max(xs), 10000)

    # Actual game data
    # Normalise centipawns to pawns on the graph for readability by dividing by 100
    plt.scatter([x / 100 for x in xs], ys, label="Lichess game data")

    # Lc0 model (see the below links)
    # https://lczero.org/dev/wiki/technical-explanation-of-leela-chess-zero/#how-does-lc0-calculate-the-cp-eval
    # https://github.com/LeelaChessZero/lc0/pull/841
    lc0_ys = [tan_model(x, 111.7, 1.562) for x in linspace]
    plt.plot(linspace / 100, lc0_ys, label="Lc0 model")

    # The current lichess model
    current_ys = [current_lichess_model(x) for x in linspace]
    plt.plot(linspace / 100, current_ys, label="Lichess model")

    # Reproducible code to train a new model
    # Prepare the data
    xs, ys = prepare_data(xs, ys, seed=1)

    # Build the model
    logistic_model = build_logistic_model(xs, ys)
    model_ys = [logistic_model(x) for x in linspace]

    # Plot the model
    plt.plot(linspace / 100, model_ys, label="New model")

    plt.legend()
    plt.xlabel("Evaluation (pawns)")
    plt.ylabel("White winning chance (%)")
    plt.show()


if __name__ == "__main__":
    main()
