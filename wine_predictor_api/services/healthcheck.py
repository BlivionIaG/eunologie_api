from typing import Tuple
from wine_predictor_api import api_config, logger


def ping() -> Tuple[str, int]:
    app_name = api_config.get("app_name")
    logger.debug(f"Just checking my {app_name}")

    return "pong", 200
