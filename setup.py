#!/usr/bin/env python3
from os.path import dirname, join
import setuptools

setuptools.setup(
    name="Eunologie API",
    version="0.0.1",
    description="API to analyse wine quality.",
    long_description=open(join(dirname(__file__), "README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/BlivionIaG/eunologie_api",
    author="BlivionIaG",
    author_email="kev29lt@gmail.com",
    license="MIT",
    package_data={"wine_predictor_api": ["specs/*.yaml"], "dataset": ["*.csv"]},
    packages=["wine_predictor_api"],
    include_package_data=True,
    install_requires=["connexion[swagger-ui]"],
    keywords=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "wine_predictor_api=wine_predictor_api.__init__:main",
        ]
    },
)
