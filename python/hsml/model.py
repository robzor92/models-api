#
#   Copyright 2020 Logical Clocks AB
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

import json

import humps
from hsml import util
from hsml.core import models_engine


class Model:
    """Metadata object representing a model in the Model Registry."""

    def __init__(
        self,
        name,
        version,
        created=None,
        environment=None,
        description=None,
        experiment_id=None,
        experiment_project_name=None,
        model_registry_id=None,
        href=None,
        expand=None,
        items=None,
        count=None,
        type=None,
    ):
        self._name = name
        self._version = version
        self._description = description
        self._created = created
        self._environment = environment
        self._experiment_id = experiment_id
        self._experiment_project_name = experiment_project_name
        self._model_registry_id = model_registry_id

    def save(self):
        """Persist the model metadata object to the model registry."""
        expectations_engine.ModelsEngine(self._featurestore_id).save(self)

    @classmethod
    def from_response_json(cls, json_dict):
        json_decamelized = humps.decamelize(json_dict)
        if "count" in json_decamelized:
            if json_decamelized["count"] == 0:
                return []
            return [cls(**expectation) for expectation in json_decamelized["items"]]
        else:
            return cls(**json_decamelized)

    def json(self):
        return json.dumps(self, cls=util.MLEncoder)

    def to_dict(self):
        return {
            "name": self._name,
            "version": self._version,
            "description": self._description
        }

    @property
    def name(self):
        """Name of the model."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def version(self):
        """Version of the model."""
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def description(self):
        """Description of the model."""
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def created(self):
        """Creation date of the model."""
        return self._created

    @created.setter
    def created(self, created):
        self._created = created

    @property
    def environment(self):
        """Anaconda environment of the model."""
        return self._environment

    @environment.setter
    def environment(self, environment):
        self._environment = environment

    @property
    def experiment_id(self):
        """experiment_id of the model."""
        return self._experiment_id

    @experiment_id.setter
    def experiment_id(self, experiment_id):
        self._experiment_id = experiment_id

    @property
    def experiment_project_name(self):
        """experiment_project_name of the model."""
        return self._experiment_project_name

    @experiment_project_name.setter
    def experiment_project_name(self, experiment_project_name):
        self._experiment_project_name = experiment_project_name