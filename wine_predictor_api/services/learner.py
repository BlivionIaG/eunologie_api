import math
import os
from typing import Tuple
import validators
import joblib
from pandas import DataFrame, read_csv
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

from wine_predictor_api import api_config, logger


def load_data() -> DataFrame:
    data_dir_path = api_config.get("data", {}).get("path")
    if not validators.url(data_dir_path) and not os.path.isfile(data_dir_path):
        raise FileNotFoundError("Data path could not be found.")

    return read_csv(data_dir_path)


def load_model():
    logger.debug("Loading model ...")
    model_dir_path = api_config.get("model", {}).get("path")

    if not validators.url(model_dir_path) and not os.path.isfile(model_dir_path):
        raise FileNotFoundError("Model path could not be found.")

    return joblib.load(model_dir_path)


def evaluate_model(model, test_data, test_target) -> float:
    logger.debug("Evaluating model ...")

    y_predicted = model.predict(test_data)
    return mean_squared_error(test_target, y_predicted)


def save_model(model, output_path: str):
    logger.debug(f"Saving model to {output_path}")

    return joblib.dump(model, output_path)


def train_model() -> Tuple[str, int]:
    try:
        dataset = load_data()
    except FileNotFoundError as e:
        logger.error(e)

        return "Error loading dataset", 404

    target = dataset["TARGET"]
    features = dataset.drop("TARGET", axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.3, random_state=0
    )

    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    mse_old = math.inf
    new_mse = evaluate_model(linear_model, X_test, y_test)
    logger.debug(f"Mean squared error: {new_mse}")

    try:
        existing_model = load_model()
        mse_old = evaluate_model(existing_model, X_test, y_test)
        logger.debug(f"Mean squared error (previous model): {mse_old}")
    except FileNotFoundError as e:
        logger.debug(f"No previous model to compare against: {e}")

    if new_mse < mse_old:
        save_model(linear_model, api_config.get("model", {}).get("path"))

        return "New model has been successfully trained and saved", 201

    return " New model has been successfully trained but was discarded", 200
