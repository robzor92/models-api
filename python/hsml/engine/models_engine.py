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
import os
import tempfile
import uuid

from hsml import client, util
from hsml.core import models_api, dataset_api
from hsml.engine import local_engine, hopsworks_engine


class Engine:

    def __init__(self):
        self._models_api = models_api.ModelsApi()
        self._dataset_api = dataset_api.DatasetApi()

        try:
            import pydoop
            self._engine = hopsworks_engine.Engine()
        except:
            self._engine = local_engine.Engine()

    def save(self, model_instance, local_model_path, await_registration=480):
        self._engine.save(model_instance, local_model_path, await_registration)

    def download(self, model_instance):
        model_name_path = os.getcwd() + "/" + str(uuid.uuid4()) + "/" + model_instance._name
        model_version_path = model_name_path + "/" + str(model_instance._version)
        if os.path.exists(model_version_path):
            raise AssertionError("Model already downloaded on path: " + model_version_path)
        else:
            if not os.path.exists(model_name_path):
                os.makedirs(model_name_path)
            dataset_model_name_path = "Models/" + model_instance._name
            dataset_model_version_path = dataset_model_name_path + "/" + str(model_instance._version)

            temp_download_dir = "/Resources" + "/" + str(uuid.uuid4())
            self._dataset_api.mkdir(temp_download_dir)
            self._dataset_api.zip(dataset_model_version_path, destination_path=temp_download_dir, block=True, timeout=480)
            zip_path = model_version_path + ".zip"
            self._dataset_api.download(temp_download_dir + "/" + str(model_instance._version) + ".zip", zip_path)
            self._dataset_api.rm(temp_download_dir)
            util.unzip(zip_path, extract_dir=model_name_path)
            os.remove(zip_path)
            return model_version_path

    def read_input_example(self, model_instance):
        try:
            tmp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
            self._dataset_api.download(model_instance._input_example, tmp_dir.name + '/inputs.json')
            with open(tmp_dir.name + '/inputs.json', 'rb') as f:
                return json.loads(f.read())
        finally:
            if tmp_dir is not None and os.path.exists(tmp_dir.name):
                tmp_dir.cleanup()

    def read_signature(self, model_instance):
        try:
            tmp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
            self._dataset_api.download(model_instance._signature, tmp_dir.name + '/signature.json')
            with open(tmp_dir.name + '/signature.json', 'rb') as f:
                return json.loads(f.read())
        finally:
            if tmp_dir is not None and os.path.exists(tmp_dir.name):
                tmp_dir.cleanup()








