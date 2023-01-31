VERSION = "0.0.1"

from typing import Any
import yaml
import logging.config
from os import getenv

from connexion import FlaskApp

from wine_predictor_api import specs


def init_logger(name=None) -> Any:
    with open(getenv("LOGGING_CONFIG", "logging.yaml")) as stream:
        logging_config = yaml.safe_load(stream)
        logging.config.dictConfig(logging_config)
        return logging.getLogger(name)


def create_app() -> FlaskApp:
    app = FlaskApp(__name__, specification_dir=specs.where())
    app.add_api("openapi_spec.yaml")

    return app


logger = init_logger()
app = create_app()
__all__ = ["logger"]


def main() -> None:
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
