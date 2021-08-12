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

from hsml.core import models_api, dataset_api


class Engine:

    def __init__(self):
        self._models_api = models_api.ModelsApi()
        self._dataset_api = dataset_api.DatasetApi()

    def save(self, model_instance, dataset_model_version_path):

        model_version_dir_exists = self._dataset_api.path_exists(dataset_model_version_path)
        if not model_version_dir_exists:
            self._dataset_api.mkdir(dataset_model_version_path)
        else:
            raise AssertionError("A model named {} with version {} already exists".format(model_instance._name, model_instance._version))
