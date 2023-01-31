from typing import Dict, Tuple
import numpy as np
from sklearn.linear_model import LinearRegression

from wine_predictor_api.services.learner import load_model
from wine_predictor_api import logger


def get_features() -> Dict:
    return {
        "fixed_acidity",
        "volatile_acidity",
        "citric_acid",
        "residual_sugar",
        "chlorides",
        "free_sulfur_dioxide",
        "total_sulfur_dioxide",
        "density",
        "pH",
        "sulphates",
        "alcohol",
    }


def prepare_data(data: Dict):
    features = get_features()
    data = [v for k, v in data.items() if k in features]
    data_np = np.array([data])

    return data_np


def estimate_wine_quality(**kwargs) -> Tuple[Dict, int]:
    try:
        data = prepare_data(kwargs)

        linear_model: LinearRegression = load_model()
        predicted_value = linear_model.predict(data).tolist()[0]

        logger.debug(f"Estimation : {predicted_value}")

        return {"estimation": round(predicted_value, 2)}, 200
    except ValueError as e:
        logger.error(e)
        return str(e), 500
    except FileNotFoundError as e:
        logger.error(e)
        return str(e), 404
    except Exception as e:
        logger.error(e)
        return f"Internal server error. Details {str(e)}", 500