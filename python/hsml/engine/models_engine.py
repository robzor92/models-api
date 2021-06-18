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
import os

from hsml import client, util
from hsml.client.exceptions import RestAPIError
from hsml.core import models_api, dataset_api


class Engine:

    def __init__(self):
        self._models_api = models_api.ModelsApi()
        self._dataset_api = dataset_api.DatasetApi()

    def save(self, model_instance, local_model_path):
        dataset_model_path = "Models/" + model_instance._name
        try:
            self._dataset_api.get(dataset_model_path)
        except RestAPIError:
            self._dataset_api.mkdir(dataset_model_path)

        if model_instance._version is None:
            current_highest_version = 0
            for item in self._dataset_api.list(dataset_model_path)['items']:
                _, file_name = os.path.split(item['attributes']['path'])
                try:
                    current_version = int(file_name)
                    if current_version > current_highest_version:
                        current_highest_version = current_version
                except:
                    pass
            model_instance._version = current_highest_version + 1

        dataset_model_version_path = "Models/" + model_instance._name + "/" + str(model_instance._version)
        model_version_dir_already_exists = False
        try:
            self._dataset_api.get(dataset_model_version_path)
            model_version_dir_already_exists = True
        except RestAPIError:
            self._dataset_api.mkdir(dataset_model_version_path)

        if model_version_dir_already_exists:
            raise Exception("bad luck, it there")

        self._dataset_api.put(model_instance)

        archive_path = util.zip(local_model_path)

        self._dataset_api.upload(archive_path, dataset_model_version_path)

        os.remove(archive_path)


