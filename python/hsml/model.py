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

import json
import shutil
import humps
from hsml import util
from hsml import client
from hsml.client.exceptions import RestAPIError
from hsml.core import models_api, dataset_api
from hsml.engine import models_engine


class Model:
    """Metadata object representing a model in the Model Registry."""

    def __init__(
        self,
        id,
        name,
        version=None,
        created=None,
        environment=None,
        description=None,
        experiment_id=None,
        experiment_project_name=None,
        metrics=None,
        program=None,
        user_full_name=None,
        signature=None,
        input_example=None,
        model_registry_id=None,
        href=None,
        expand=None,
        items=None,
        count=None,
        type=None,
    ):
        if id is None:
            self._id = name + "_" + str(version)
        else:
            self._id = id

        self._name = name
        self._version = version

        if description is None:
            self._description = 'A collection of models for ' + name
        else:
            self._description = description

        self._created = created
        self._environment = environment
        self._experiment_id = experiment_id
        self._experiment_project_name = experiment_project_name
        self._metrics = metrics
        self._program = program
        self._user_full_name = user_full_name
        self._input_example = input_example
        self._signature = signature
        self._model_registry_id = model_registry_id

        self._models_api = models_api.ModelsApi()
        self._dataset_api = dataset_api.DatasetApi()
        self._models_engine = models_engine.Engine()


    def save(self, model_path):
        """Persist the model metadata object to the model registry."""
        self._models_engine.save(self, model_path)

    def delete(self):
        """Delete the model

        !!! danger "Potentially dangerous operation"
            This operation drops all metadata associated with **this version** of the
            model **and** in addition to the model artifacts.

        # Raises
            `RestAPIError`.
        """
        self._models_api.delete(self)

    @classmethod
    def from_response_json(cls, json_dict):
        json_decamelized = humps.decamelize(json_dict)
        if "count" in json_decamelized:
            if json_decamelized["count"] == 0:
                return []
            return [cls(**expectation) for expectation in json_decamelized["items"]]
        else:
            return cls(**json_decamelized)
            
    def update_from_response_json(self, json_dict):
        json_decamelized = humps.decamelize(json_dict)
        _ = json_decamelized.pop("type")
        # here we lose the information that the user set, e.g. write_options
        self.__init__(**json_decamelized)
        return self

    def json(self):
        return json.dumps(self, cls=util.MLEncoder)

    def to_dict(self):
        return {
            "id": self._name + "_" + str(self._version),
            "name": self._name,
            "version": self._version,
            "description": self._description,
            "inputExample": self._input_example
        }

    @property
    def id(self):
        """Id of the model."""
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

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

    @property
    def metrics(self):
        """metrics of the model."""
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        self._metrics = metrics

    @property
    def program(self):
        """program of the model."""
        return self._program

    @program.setter
    def program(self, program):
        self._program = program

    @property
    def user_full_name(self):
        """user_full_name of the model."""
        return self._user_full_name

    @user_full_name.setter
    def user_full_name(self, user_full_name):
        self._user_full_name = user_full_name

    @property
    def input_example(self):
        """input_example of the model."""
        if self._input_example is not None and isinstance(self._input_example, str):
            self._dataset_api.download(self._input_example)
            with open('inputs.json', 'rb') as f:
                self._input_example = json.loads(f.read())
        return self._input_example

    @input_example.setter
    def input_example(self, input_example):
        self._input_example = input_example

    @property
    def signature(self):
        """signature of the model."""
        return self._signature

    @signature.setter
    def signature(self, signature):
        self._signature = signature
