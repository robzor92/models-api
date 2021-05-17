import os
import imp
from setuptools import setup, find_packages


__version__ = imp.load_source(
    "hsmr.version", os.path.join("hsmr", "version.py")
).__version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="hsmr",
    version=__version__,
    install_requires=[],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "black"],
        "docs": [
            "mkdocs==1.1.2",
            "mkdocs-material==6.2.2",
            "mike==0.5.5",
            "keras-autodoc",
            "markdown-include"]
    },
    author="Logical Clocks AB",
    author_email="robin@logicalclocks.com",
    description="HSMR: An environment independent client to interact with the Hopsworks Model Registry and Model Serving",
    license="Apache License 2.0",
    keywords="Hopsworks, Feature Store, TensorFlow, PyTorch, Machine Learning, MLOps, DataOps",
    url="https://github.com/logicalclocks/models-api",
    download_url="https://github.com/logicalclocks/models-api/releases/tag/"
    + __version__,
    packages=find_packages(),
    long_description=read("../README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ],
)
