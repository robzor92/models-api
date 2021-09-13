# Hopsworks Model Registry

<p align="center">
  <a href="https://community.hopsworks.ai"><img
    src="https://img.shields.io/discourse/users?label=Hopsworks%20Community&server=https%3A%2F%2Fcommunity.hopsworks.ai"
    alt="Hopsworks Community"
  /></a>
    <a href="https://docs.hopsworks.ai"><img
    src="https://img.shields.io/badge/docs-HSML-orange"
    alt="Hopsworks Feature Store Documentation"
  /></a>
  <a href="https://pypi.org/project/hsml/"><img
    src="https://img.shields.io/pypi/v/hsml?color=blue"
    alt="PyPiStatus"
  /></a>
  <a href="https://archiva.hops.works/#artifact/com.logicalclocks/hsml"><img
    src="https://img.shields.io/badge/java-HSML-green"
    alt="Scala/Java Artifacts"
  /></a>
  <a href="https://pepy.tech/project/hsml/month"><img
    src="https://pepy.tech/badge/hsml/month"
    alt="Downloads"
  /></a>
  <a href="https://github.com/psf/black"><img
    src="https://img.shields.io/badge/code%20style-black-000000.svg"
    alt="CodeStyle"
  /></a>
  <a><img
    src="https://img.shields.io/pypi/l/hsml?color=green"
    alt="License"
  /></a>
</p>

HSML is the library to interact with the Hopsworks Model Registry. The library makes it easy to export models with meaningful metadata and manage versioning.

The library automatically configures itself based on the environment it is run.
However, to connect from an external environment such as Databricks or AWS Sagemaker,
additional connection information, such as host and port, is required. For more information about the setup from external environments, see the setup section.

## Getting Started On Hopsworks

Instantiate a connection and get the project model registry handler
```python
import hsml

connection = hsml.connection()
mr = connection.get_model_registry()
```

Create a new model
```python
model = mr.tensorflow.create_model("mnist",
                        version=1,
                        description="A model description",
                        metrics={"accuracy": 0.94, "loss": 0.0432})

mr.save("model_directory")
```

Get the exported model
```python
mnist_1 = mr.get_model(name="mnist", version=1)
```

Download all the model artifacts
```python
local_directory = mnist_1.download()
```

Delete the model from the model registry
```python
mnist_1.delete()
```

You can find more examples on how to use the library in our [hops-examples](https://github.com/logicalclocks/hops-examples) repository.

## Documentation

Documentation is available at [Hopsworks Model Registry Documentation](https://docs.hopsworks.ai/).

## Issues

For general questions about the usage of Hopsworks and the Model Registry please open a topic on [Hopsworks Community](https://community.hopsworks.ai/).

Please report any issue using [Github issue tracking](https://github.com/logicalclocks/machine-learning-api/issues).


## Contributing

If you would like to contribute to this library, please see the [Contribution Guidelines](CONTRIBUTING.md).
