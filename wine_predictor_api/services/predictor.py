from typing import Dict, Set, Tuple
import numpy as np
from sklearn.linear_model import LinearRegression

from wine_predictor_api import logger
import wine_predictor_api


def get_features() -> Set[str]:
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
    t_data = [v for k, v in data.items() if k in features]
    data_np = np.array([t_data])

    return data_np


def estimate_wine_quality(**kwargs) -> Tuple[Dict, int]:
    try:
        data = prepare_data(kwargs)

        linear_model: LinearRegression = (
            wine_predictor_api.services.learner.load_model()
        )
        predicted_value = linear_model.predict(data).tolist()[0]

        logger.debug(f"Estimation : {predicted_value}")

        return {"estimation": round(predicted_value, 2)}, 200
    except ValueError as e:
        logger.error(e)
        return {"error": str(e)}, 500
    except FileNotFoundError as e:
        logger.error(e)
        return {"error": str(e)}, 404
    except Exception as e:
        logger.error(e)
        return {"error": f"Internal server error. Details {str(e)}"}, 500
