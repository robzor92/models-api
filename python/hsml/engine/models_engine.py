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
import datetime
import importlib.util

from hsml import client, util
from hsml.client.exceptions import RestApiError
from hsml.core import models_api, dataset_api


class Engine:

    def __init__(self):
        self._models_api = models_api.ModelsApi()
        self._dataset_api = dataset_api.DatasetApi()

    def save(self, model_instance, local_model_path):
        #self._dataset_api.mkdir()
        #attach xattr
        dataset_model_path = "Models/" + self._name
        try:
            self._dataset_api.get(dataset_model_path)
        except RestAPIError:
            self._dataset_api.mkdir(dataset_model_path)

        version=1
        if self._version is None:
            resp = self._dataset_api.get(dataset_model_path)
            print(resp)
        self._version = version

        archive_path = util.zip(local_model_path)
        self._dataset_api.upload(archive_path, "Models/" + self._name + "/" + str(self._version))
