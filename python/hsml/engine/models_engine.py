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
import time
from typing import Union
import numpy as np
import pandas as pd
import tempfile
import uuid

from hsml import client, util
from hsml.client.exceptions import RestAPIError
from hsml.core import models_api, dataset_api


class Engine:

    def __init__(self):
        self._models_api = models_api.ModelsApi()
        self._dataset_api = dataset_api.DatasetApi()

    def save(self, model_instance, local_model_path, await_registration=480):
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
            raise RestAPIError("A model named {} with version {} already exists".format(model_instance._name, model_instance._version))

        model_query_params = {}

        if 'HOPSWORKS_JOB_NAME' in os.environ:
            model_query_params['jobName'] = os.environ['HOPSWORKS_JOB_NAME']
        elif 'HOPSWORKS_KERNEL_ID' in os.environ:
            model_query_params['kernelId'] = os.environ['HOPSWORKS_KERNEL_ID']

        if 'ML_ID' in os.environ:
            model_instance._experiment_id = os.environ['ML_ID']

        _client = client.get_instance()
        model_instance._project_name = _client._project_name
        model_instance._experiment_project_name = _client._project_name

        if model_instance.input_example is not None:
            input_example_path = os.getcwd() + "/input_example.json"
            input_example = util.input_example_to_json(model_instance.input_example)

            with open(input_example_path, 'w+') as out:
                json.dump(input_example, out, cls=util.NumpyEncoder)

            self._dataset_api.upload(input_example_path, dataset_model_version_path)
            os.remove(input_example_path)
            model_instance.input_example = dataset_model_version_path + "/input_example.json"

        self._models_api.put(model_instance, model_query_params)

        try:
            zip_out_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
            archive_path = util.zip(zip_out_dir.name, local_model_path)
            self._dataset_api.upload(archive_path, dataset_model_version_path)
        except:
            raise
        finally:
            zip_out_dir.cleanup()

        extracted_archive_path = dataset_model_version_path + "/" + os.path.basename(archive_path)

        self._dataset_api.unzip(extracted_archive_path, block=True, timeout=480)

        self._dataset_api.rm(extracted_archive_path)

        unzipped_model_dir = dataset_model_version_path + "/" + os.path.splitext(os.path.basename(archive_path))[0]

        for artifact in os.listdir(local_model_path):
            _, file_name = os.path.split(artifact)
            self._dataset_api.move(unzipped_model_dir + "/" + file_name,
            dataset_model_version_path + "/" + file_name)

        self._dataset_api.rm(unzipped_model_dir)

        if await_registration > 0:
                start_time = time.time()
                sleep_seconds = 5
                for i in range(int(await_registration/sleep_seconds)):
                    try:
                        time.sleep(sleep_seconds)
                        print("Polling " + model_instance.name + " version " + str(model_instance.version) + " for model availability.")
                        return self._models_api.get(name=model_instance.name, version=model_instance.version)
                        print(model_name + " not ready yet, retrying in " + str(sleep_seconds) + " seconds.")
                    except ModelNotFound:
                        pass
                print("Model not available during polling, set a higher value for await_registration to wait longer.")

    def download(self, model_instance):
        model_name_path = os.getcwd() + "/" + str(uuid.uuid4()) + "/" + model_instance._name
        model_version_path = model_name_path + "/" + str(model_instance._version)
        if os.path.exists(model_version_path):
            print("error")
            raise AssertionError("Model already downloaded on path: " + model_version_path)
        else:
            if not os.path.exists(model_name_path):
                print("dir yo1")
                os.makedirs(model_name_path)
            dataset_model_name_path = "Models/" + model_instance._name
            dataset_model_version_path = dataset_model_name_path + "/" + str(model_instance._version)

            temp_download_dir = dataset_model_name_path + str(uuid.uuid4())
            self._dataset_api.mkdir(temp_download_dir)

            self._dataset_api.mkdir(dataset_model_version_path)
            print("dir yo2")
            self._dataset_api.zip(dataset_model_version_path, destination_path=temp_download_dir, block=True, timeout=480)
            print("dir yo3")
            zip_path = model_version_path + ".zip"
            self._dataset_api.download(dataset_model_version_path + ".zip", zip_path)
            print("dir yo4")
            self._dataset_api.rm(dataset_model_version_path + ".zip")
            print("dir yo5")
            util.unzip(zip_path, extract_dir=model_name_path)
            print("dir yo6")
            os.remove(zip_path)
            return model_version_path

    def read_input_example(self, model_instance, input_example_path):
        try:
            tmp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
            self._dataset_api.download(input_example_path, tmp_dir.name + '/inputs.json')
            with open(tmp_dir.name + '/inputs.json', 'rb') as f:
                return json.loads(f.read())
        finally:
            if tmp_dir is not None and os.path.exists(tmp_dir.name):
                tmp_dir.cleanup()





