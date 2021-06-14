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

import warnings
import humps
import numpy
import datetime
from typing import Optional, Union, List, Dict, TypeVar

from hsml import (
    model,
    util
)
from hsml.core import (
    models_api
)

class ModelRegistry:
    DEFAULT_VERSION = 1

    def __init__(
        self,
        project_name,
        project_id,
        num_models=None
    ):
        self._project_name = project_name
        self._project_id = project_id
        self._num_models = num_models

        self._models_api = models_api.ModelsApi

    @classmethod
    def from_response_json(cls, json_dict):
        json_decamelized = humps.decamelize(json_dict)
        return cls(**json_decamelized)

    def get_model(self, name: str, version: int = None):
        """Get a model entity from the model registry.

        Getting a model from the Model Registry means getting its metadata handle
        so you can subsequently download the model artifacts in consecutive download() call.

        # Arguments
            name: Name of the model to get.
            version: Version of the model to retrieve, defaults to `None` and will
                return the `version=1`.

        # Returns
            `Model`: The model metadata object.

        # Raises
            `RestAPIError`: If unable to retrieve model from the model registry.

        """
        if version is None:
            warnings.warn(
                "No version provided for getting feature group `{}`, defaulting to `{}`.".format(
                    name, self.DEFAULT_VERSION
                ),
                util.VersionWarning,
            )
            version = self.DEFAULT_VERSION
        return self._models_api.get(
            name, version
        )

    @property
    def project_name(self):
        """Name of the project in which the model registry is located."""
        return self._project_name

    @property
    def project_id(self):
        """Id of the project in which the model registry is located."""
        return self._project_id

    @property
    def num_models(self):
        """Number of models in the model registry."""
        return self._num_models
