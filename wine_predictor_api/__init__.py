VERSION = "0.0.1"

from typing import Any, Dict
import yaml
import json
import logging.config
from os import getenv, environ

from connexion import FlaskApp
from jinja2 import Environment, FileSystemLoader

from wine_predictor_api import specs


def init_config():
    with open(getenv("API_CONFIG", "config.json")) as stream:
        return json.load(stream)


def init_logger(name=None) -> Any:
    with open(getenv("LOGGING_CONFIG", "logging.yaml")) as stream:
        logging_config = yaml.safe_load(stream)
        logging.config.dictConfig(logging_config)
        return logging.getLogger(name)


# def create_app() -> FlaskApp:
#     env = Environment(loader=FileSystemLoader(specs.where()))
#     template = env.get_template("openapi_spec.yaml.j2")

#     spec_options = api_config.get("spec_options", {})
#     spec_options["version"] = environ.get("API_VERSION", "0.0.1")

#     specifications = yaml.safe_load(template.render(**spec_options))

#     app = FlaskApp(__name__, specification_dir=specs.where())
#     app.add_api(specifications, arguments=spec_options)

#     return app


def create_app() -> FlaskApp:
    spec_options = api_config.get("spec_options", {})
    spec_options["version"] = environ.get("API_VERSION", "0.0.1")

    app = FlaskApp(__name__, specification_dir=specs.where())
    app.add_api("openapi_spec.yaml.j2", arguments=spec_options)

    return app


def main() -> None:
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()

api_config: Dict[str, Any] = init_config()
logger = init_logger()

app = create_app()

__all__ = ["logger", "api_config"]
