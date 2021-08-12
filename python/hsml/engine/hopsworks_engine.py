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

class Engine:

    def __init__(self):
        self._models_api = models_api.ModelsApi()
        self._dataset_api = dataset_api.DatasetApi()
        self._native_hdfs_api = native_hdfs_api.NativeHdfsApi()

    def save(self, model_instance, dataset_model_version_path):

        project_path = self._native_hdfs_api.project_path()

        model_version_dir_hdfs = project_path + "/" + dataset_model_version_path

        # If version directory already exists and we are not overwriting it then fail
        if self._native_hdfs_api.exists(model_version_dir_hdfs):
            raise AssertionError("A model named {} with version {} already exists".format(model_instance._name, model_instance._version))

        # At this point we can create the version directory if it does not exist
        if not self._native_hdfs_api.exists(model_version_dir_hdfs):
            self._native_hdfs_api.mkdir(model_version_dir_hdfs)