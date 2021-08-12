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

from hsml.core import models_api, dataset_api, native_hdfs_api
import os

class Engine:

    def __init__(self):
        self._models_api = models_api.ModelsApi()
        self._dataset_api = dataset_api.DatasetApi()
        self._native_hdfs_api = native_hdfs_api.NativeHdfsApi()

    def save(self, model_instance, local_model_path):

        project_path = self._native_hdfs_api.project_path()

        model_dir_hdfs = project_path + "/Models/" + model_instance.name

        if not self._native_hdfs_api.exists(model_dir_hdfs):
            self._native_hdfs_api.mkdir(model_dir_hdfs)
            self._native_hdfs_api.chmod(model_dir_hdfs, "ug+rwx")

        # User did not specify model_version, pick the current highest version + 1, set to 1 if no model exists
        version_list = []
        if not model_instance.version and self._native_hdfs_api.exists(model_dir_hdfs):
            model_version_directories = self._native_hdfs_api.ls(model_dir_hdfs)
            for version_dir in model_version_directories:
                try:
                    if self._native_hdfs_api.exists.isdir(version_dir):
                        version_list.append(int(version_dir[len(model_dir_hdfs):]))
                except:
                    pass
            if len(version_list) > 0:
                model_version = max(version_list) + 1

        if not model_version:
            model_version = 1

        # Path to directory in HDFS to put the model files
        model_version_dir_hdfs = model_dir_hdfs + str(model_version)

        # If version directory already exists and we are not overwriting it then fail
        if self._native_hdfs_api.exists(model_version_dir_hdfs):
            raise AssertionError("Could not create model directory: {}, the path already exists".format(model_version_dir_hdfs))

        # At this point we can create the version directory if it does not exist
        if not self._native_hdfs_api.exists(model_version_dir_hdfs):
            self._native_hdfs_api.mkdir(model_version_dir_hdfs)

        return