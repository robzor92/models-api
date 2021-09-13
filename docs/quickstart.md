# Quickstart Guide

The Hopsworks model registry is a centralized repository, within an organization, to manage machine learning models. A model is the product of training a machine learning algorithm with training data. It could be an image classifier used to detect objects in an image, such as for example detecting cancer in an MRI scan.

<p align="center">
  <figure>
    <a  href="../assets/images/quickstart.png">
      <img src="../assets/images/quickstart.png" alt="The Hopsworks Feature Store">
    </a>
    <figcaption>The Hopsworks Feature Store</figcaption>
  </figure>
</p>

In this Quickstart Guide we are going to focus on the left side of the picture above. In particular how data scientists can create models and publish them to the model registry to make them available for further development and serving.

### HSFS library

The Hopsworks model registry library is called `hsml` (**H**opswork**s** **M**achine **L**earning).
The library is Apache V2 licensed and available [here](https://github.com/logicalclocks/machine-learning-api). The library is currently available for Python.
If you want to connect to the Model Registry from outside Hopsworks, see our [integration guides](setup.md).

The library is build around metadata-objects, representing entities within the Model Registry. You can modify metadata by changing it in the metadata-objects and subsequently persisting it to the Model Registry. In fact, the Model Registry itself is also represented by an object. Furthermore, these objects have methods to save model artifacts along with the entities in the model registry.

### Guide Notebooks

This guide is based on a [series of notebooks](https://github.com/logicalclocks/hops-examples/tree/master/notebooks/ml/hsml), which is available in the Deep Learning Demo Tour Project on Hopsworks.

### Connection, Project and Model Registry

The first step is to establish a connection with your Hopsworks Model Registry instance and retrieve the object that represents the Model Registry you'll be working with.

By default `connection.get_model_registry()` returns the model registry of the project you are working with. However, it accepts also a project name as parameter to select a different model registry.

=== "Python"

    ```python
    import hsml

    # Create a connection
    connection = hsml.connection()

    # Get the model registry handle for the project's model registry
    mr = connection.get_model_registry()
    ```

### Models

Assuming you have done some model training, having export a model to a directory on a local file path, the model artifacts and additional metadata can now be saved to the Model Registry. See the [example notebooks](https://github.com/logicalclocks/hops-examples/blob/master/notebooks/ml/hsml).

#### Creation

Create a model named `mnist`. As you can see, you have the possibility to make settings on the Model, such as the `version` number, or `metrics` parameter which is set to attach model training metrics on the model. The [Model Guide](generated/model.md) guides through the full configuration of Models.

=== "Python"

    ```python
    mnist_model_meta = mr.create_model(name="mnist",
        version=1,
        metrics={"accuracy": 0.94},
        description="mnist model description")
    ```

Up to this point we have just created the metadata object representing the model. However, we haven't saved the model in the model registry yet. To do so, we can call the method `save` on the metadata object created in the cell above.
The `save` method takes a single parameter which is the path to the directory on the local filesystem which contains all your model artifacts.

=== "Python"

    ```python
    mnist_model_meta.save("/tmp/model_directory")
    ```

#### Retrieval

If there were models previously created in your Model Registry, or you want to pick up where you left off before, you can retrieve and read models in a similar fashion as creating them:
Using the Model Registry object, you can retrieve handles to the entities, such as models, in the Model Registry. By default, this will return the first version of an entity, if you want a more recent version, you need to specify the version.

=== "Python"

    ```python
    mnist_model_meta = mr.get_model('mnist', version=1)

    # Download the model
    model_download_path = mnist_model_meta.download()

    # Load the model
    tf.saved_model.load(model_download_path)
    ```

To seamlessly combine HSML with model serving components the library makes it simple to also query for the best performing model. In this instance, we get the best model version with the highest `accuracy` metric attached.

=== "Python"

    ```python
    mnist_model_meta = mr.get_best_model('mnist', 'accuracy', 'max')

    ```

#### Input examples and Signatures

HSML provides an API similar to Pandas to join feature groups together and to select features from different feature groups.
The easies query you can write is by selecting all the features from a feature group and join them with all the features of another feature group.

You can use the `select_all()` method of a feature group to select all its features. HSFS relies on the Hopsworks feature store to identify which features of the two feature groups to use as joining condition.
If you don't specify anything, Hopsworks will use the largest matching subset of primary keys with the same name.

In the example below, `sales_fg` has `store`, `dept` and `date` as composite primary key while `exogenous_fg` has only `store` and `date`. So Hopsworks will set as joining condition `store` and `date`.

=== "Python"

    ```python
    sales_fg = fs.get_feature_group('sales_fg')
    exogenous_fg = fs.get_feature_group('exogenous_fg')

    query = sales_fg.select_all().join(exogenous_fg.select_all())

    # print first 5 rows of the query
    query.show(5)
    ```

=== "Scala"

    ```scala
    val exogenousFg = fs.getFeatureGroup("exogenous_fg")
    val salesFg = fs.getFeatureGroup("sales_fg")

    val query = salesFg.selectAll().join(exogenousFg.selectAll())

    // print first 5 rows of the query
    query.show(5)
    ```

For a more complex joins, and details about overwriting the join keys and join type, the programming interface guide explains the `Query` interface as well as

### Training Datasets

Once a Data Scientist has found the features she needs for her model, she can create a training dataset to materialize the features in the desired file format. The Hopsworks Feature Store supports a variety of file formats, matching the Data Scientists' favourite Machine Learning Frameworks.

#### Creation

You can either create a training dataset from a `Query` object or directly from a Spark or Pandas DataFrame. Spark and Pandas give you more flexibility, but it has drawbacks for reproducability at inference time, when the Feature Vector needs to be reconstructed. The idea of the Feature Store is to have ready-engineered features available for Data Scientists to be selected for training datasets. With this assumption, it should not be necessary to perform additional engineering, but instead joining, filtering and point in time querying should be enough to generate training datasets.

=== "Python"

    ```python
    store_fg = fs.get_feature_group("store_fg")
    sales_fg = fs.get_feature_group('sales_fg')
    exogenous_fg = fs.get_feature_group('exogenous_fg')

    query = sales_fg.select_all() \
        .join(store_fg.select_all()) \
        .join(exogenous_fg.select(['fuel_price', 'unemployment', 'cpi']))

    td = fs.create_training_dataset(
        name = "sales_model",
        description = "Dataset to train the sales model",
        data_format = "tfrecord",
        splits = {"train": 0.7, "test": 0.2, "validate": 0.1},
        version = 1)

    td.save(query)
    ```

=== "Scala"

    ```scala
    val storeFg = fs.getFeatureGroup("store_fg")
    val exogenousFg = fs.getFeatureGroup("exogenous_fg")
    val salesFg = fs.getFeatureGroup("sales_fg")

    query = (salesFg.selectAll()
        .join(storeFg.selectAll())
        .join(exogenousFg.select(Seq("fuel_price", "unemployment", "cpi").asJava)))

    val td = (fs.createTrainingDataset()
                          .name("sales_model")
                          .description("Dataset to train the sales model")
                          .version(1)
                          .dataFormat(DataFormat.TFRECORD)
                          .splits(Map("train" -> Double.box(0.7), "test" -> Double.box(0.2), "validate" -> Double.box(0.1))
                          .build())

    td.save(query)
    ```

#### Retrieval

If you want to use a previously created training dataset to train a machine learning model, you can get the training dataset similarly to how you get a feature group.

=== "Python"

    ```python
    td = fs.get_training_dataset("sales_model")

    df = td.read(split="train")
    ```

=== "Scala"

    ```scala
    val td = fs.getTrainingDataset("sales_model")

    val df = td.read("train")
    ```

Either you read the data into a DataFrame again, or you use the provided utility methods, to instantiate for example a [`tf.data.Dataset`](https://www.tensorflow.org/guide/data), which can directly be passed to a TensorFlow model.

=== "Python"

    ```python
    train_input_feeder = training_dataset.feed(target_name="label",
                                            split="train",
                                            is_training=True)
    train_input = train_input_feeder.tf_record_dataset()
    ```

=== "Scala"

    This functionality is only available in the Python API.
