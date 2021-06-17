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

import math
import os
import shutil

from hsml import client, util


class DatasetApi:
    DEFAULT_FLOW_CHUNK_SIZE = 1048576

    def upload(self, local_path, upload_path):

        local_abs_path = os.path.join(path, name)

        size = os.path.getsize(local_abs_path)

        num_chunks = math.ceil(size / self.DEFAULT_FLOW_CHUNK_SIZE)

        base_params = self._get_flow_base_params(name, num_chunks, size)

        chunk_number = 1
        with open(local_abs_path) as f:
            while True:
              chunk = f.read(self.DEFAULT_FLOW_CHUNK_SIZE)
              if not chunk:
                  break

              query_params = base_params
              query_params["flowCurrentChunkSize"] = len(chunk)
              query_params["flowChunkNumber"] = chunk_number

              self._upload_request(
                  query_params, path, name, chunk
              )

              chunk_number += 1


    def _get_flow_base_params(self, file_name, num_chunks, size):
        return {
            "templateId": -1,
            "flowChunkSize": self.DEFAULT_FLOW_CHUNK_SIZE,
            "flowTotalSize": size,
            "flowIdentifier": str(size) + "_" + file_name,
            "flowFilename": file_name,
            "flowRelativePath": file_name,
            "flowTotalChunks": num_chunks,
        }

    def _upload_request(self, params, path, file_name, chunk):
        _client = client.get_instance()
        path_params = ["project", _client._project_id, "dataset", "upload", path]

        # Flow configuration params are sent as form data
        _client._send_request(
            "POST", path_params, data=params, files={"file": (file_name, chunk)}
        )

    def get(self, remote_path):
        """Save model metadata to the model registry.

        :param model_instance: metadata object of feature group to be saved
        :type model_instance: Model
        :return: updated metadata object of the model
        :rtype: Model
        """
        _client = client.get_instance()
        path_params = [
            "project",
            _client._project_id,
            "dataset",
            remote_path
        ]
        query_params = {'action': 'listing'}
        headers = {"content-type": "application/json"}
        return model_instance.update_from_response_json(
            _client._send_request(
                "GET",
                path_params,
                headers=headers,
                query_params=query_params,
                data=model_instance.json(),
            ),
        )