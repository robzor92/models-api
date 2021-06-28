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
from typing import Union
import numpy as np
import tempfile

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

        model_query_params = {}

        if 'HOPSWORKS_JOB_NAME' in os.environ:
            model_query_params['jobName'] = os.environ['HOPSWORKS_JOB_NAME']
        elif 'HOPSWORKS_KERNEL_ID' in os.environ:
            model_query_params['kernelId'] = os.environ['HOPSWORKS_KERNEL_ID']

        if model_instance.input_example is not None:
            input_example_path = os.getcwd() + "/input_example.json"
            input_example = self._handle_tensor_input(model_instance.input_example)
            with open(input_example_path, 'w+') as out:
                json.dump(input_example, out, cls=util.NumpyEncoder)
            self._dataset_api.upload(input_example_path, dataset_model_version_path)
            os.remove(input_example_path)
            model_instance.input_example = dataset_model_version_path + "/input_example.json"

        self._models_api.put(model_instance, model_query_params)

        archive_path = util.zip(local_model_path)

        self._dataset_api.upload(archive_path, dataset_model_version_path)

        os.remove(archive_path)

        extracted_archive_path = dataset_model_version_path + "/" + os.path.basename(local_model_path)
        uploaded_archive_path = extracted_archive_path + ".zip"

        self._dataset_api.unzip(uploaded_archive_path, block=True, timeout=480)

        self._dataset_api.rm(uploaded_archive_path)

        for artifact in os.listdir(local_model_path):
            _, file_name = os.path.split(artifact)
            self._dataset_api.move(extracted_archive_path + "/" + file_name,
            dataset_model_version_path + "/" + file_name)

        self._dataset_api.rm(extracted_archive_path)

    def _handle_tensor_input(self, input_tensor: Union[np.ndarray, dict]):
        if isinstance(input_tensor, dict):
            result = {}
            for name in input_tensor.keys():
                result[name] = input_tensor[name].tolist()
            return {"inputs": result}
        else:
            return {"inputs": input_tensor.tolist()}

    def read_input_example(self, model_instance, input_example_path):
        try:
            tmp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
            self._dataset_api.download(input_example_path, tmp_dir.name + '/inputs.json')
            with open(tmp_dir.name + '/inputs.json', 'rb') as f:
                return json.loads(f.read())
        finally:
            if tmp_dir is not None and os.path.exists(tmp_dir.name):
                tmp_dir.cleanup()





