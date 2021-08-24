#
#   Copyright 2021 Logical Clocks AB
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from typing import Optional, Union, TypeVar
import pandas
import numpy
from hsml.utils.signature import Signature
from hsml.framework.tensorflow.model import Model


def create_model(
    name: str,
    version: Optional[int] = None,
    metrics: Optional[dict] = None,
    description: Optional[str] = None,
    input_example: Optional[Union[pandas.core.frame.DataFrame, numpy.ndarray]] = None,
    signature: Optional[Signature] = None,
    training_dataset: Optional[
        TypeVar("hsfs.training_dataset.TrainingDataset")  # noqa: F821
    ] = None,
):
    """Create a model metadata object.

    !!! note "Lazy"
        This method is lazy and does not persist any metadata or uploads model artifacts in the
        model registry on its own. To save the model object and the model artifacts, call the `save()` method with a
        local file path to the directory containing the model artifacts.

    # Arguments
        name: Name of the feature group to create.
        version: Version of the feature group to retrieve, defaults to `None` and
            will create the feature group with incremented version from the last
            version in the feature store.
        description: A string describing the contents of the feature group to
            improve discoverability for Data Scientists, defaults to empty string
            `""`.
        online_enabled: Define whether the feature group should be made available
            also in the online feature store for low latency access, defaults to
            `False`.
        time_travel_format: Format used for time travel, defaults to `"HUDI"`.
        partition_key: A list of feature names to be used as partition key when
            writing the feature data to the offline storage, defaults to empty list
            `[]`.
        primary_key: A list of feature names to be used as primary key for the
            feature group. This primary key can be a composite key of multiple
            features and will be used as joining key, if not specified otherwise.
            Defaults to empty list `[]`, and the first column of the DataFrame will
            be used as primary key.
        hudi_precombine_key: A feature name to be used as a precombine key for the `"HUDI"`
            feature group. Defaults to `None`. If feature group has time travel format
            `"HUDI"` and hudi precombine key was not specified then the first primary key of
            the feature group will be used as hudi precombine key.
        features: Optionally, define the schema of the feature group manually as a
            list of `Feature` objects. Defaults to empty list `[]` and will use the
            schema information of the DataFrame provided in the `save` method.
        statistics_config: A configuration object, or a dictionary with keys
            "`enabled`" to generally enable descriptive statistics computation for
            this feature group, `"correlations`" to turn on feature correlation
            computation and `"histograms"` to compute feature value frequencies. The
            values should be booleans indicating the setting. To fully turn off
            statistics computation pass `statistics_config=False`. Defaults to
            `None` and will compute only descriptive statistics.
        validation_type: Optionally, set the validation type to one of "NONE", "STRICT",
            "WARNING", "ALL". Determines the mode in which data validation is applied on
             ingested or already existing feature group data.
        expectations: Optionally, a list of expectations to be attached to the feature group.
            The expectations list contains Expectation metadata objects which can be retrieved with
            the `get_expectation()` and `get_expectations()` functions.

    # Returns
        `Model`. The model metadata object.
    """
    return Model(
        id=None,
        name=name,
        version=version,
        description=description,
        metrics=metrics,
        input_example=input_example,
        signature=signature,
        training_dataset=training_dataset,
    )
