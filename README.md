# Hopsworks Feature Store

<p align="center">
  <a href="https://community.hopsworks.ai"><img
    src="https://img.shields.io/discourse/users?label=Hopsworks%20Community&server=https%3A%2F%2Fcommunity.hopsworks.ai"
    alt="Hopsworks Community"
  /></a>
    <a href="https://docs.hopsworks.ai"><img
    src="https://img.shields.io/badge/docs-HSFS-orange"
    alt="Hopsworks Feature Store Documentation"
  /></a>
  <a href="https://pypi.org/project/hsfs/"><img
    src="https://img.shields.io/pypi/v/hsfs?color=blue"
    alt="PyPiStatus"
  /></a>
  <a href="https://archiva.hops.works/#artifact/com.logicalclocks/hsfs"><img
    src="https://img.shields.io/badge/java-HSFS-green"
    alt="Scala/Java Artifacts"
  /></a>
  <a href="https://pepy.tech/project/hsfs/month"><img
    src="https://pepy.tech/badge/hsfs/month"
    alt="Downloads"
  /></a>
  <a href="https://github.com/psf/black"><img
    src="https://img.shields.io/badge/code%20style-black-000000.svg"
    alt="CodeStyle"
  /></a>
  <a><img
    src="https://img.shields.io/pypi/l/hsfs?color=green"
    alt="License"
  /></a>
</p>

HSFS is the library to interact with the Hopsworks Feature Store. The library makes creating new features, feature groups and training datasets easy.

The library is environment independent and can be used in two modes:

- Spark mode: For data engineering jobs that create and write features into the feature store or generate training datasets. It requires a Spark environment such as the one provided in the Hopsworks platform or Databricks. In Spark mode, HSFS provides bindings both for Python and JVM languages.

- Python mode: For data science jobs to explore the features available in the feature store, generate training datasets and feed them in a training pipeline. Python mode requires just a Python interpreter and can be used both in Hopsworks from Python Jobs/Jupyter Kernels, Amazon SageMaker or KubeFlow.

The library automatically configures itself based on the environment it is run.
However, to connect from an external environment such as Databricks or AWS Sagemaker,
additional connection information, such as host and port, is required. For more information about the setup from external environments, see the setup section.

## Getting Started On Hopsworks



You can find more examples on how to use the library in our [hops-examples](https://github.com/logicalclocks/hops-examples) repository.

## Documentation

Documentation is available at [Hopsworks Model Registry Documentation](https://docs.hopsworks.ai/).

## Issues

For general questions about the usage of Hopsworks and the Feature Store please open a topic on [Hopsworks Community](https://community.hopsworks.ai/).

Please report any issue using [Github issue tracking](https://github.com/logicalclocks/machine-learning-api/issues).


## Contributing

If you would like to contribute to this library, please see the [Contribution Guidelines](CONTRIBUTING.md).
