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
from hsml.client.exceptions import RestAPIError
import time

from hsml import client, util

class DatasetApi:
    DEFAULT_FLOW_CHUNK_SIZE = 1048576

    def upload(self, local_abs_path, upload_path):

        size = os.path.getsize(local_abs_path)

        _, file_name = os.path.split(local_abs_path)

        num_chunks = math.ceil(size / self.DEFAULT_FLOW_CHUNK_SIZE)

        base_params = self._get_flow_base_params(file_name, num_chunks, size)

        chunk_number = 1
        with open(local_abs_path, 'rb') as f:
            while True:
              chunk = f.read(self.DEFAULT_FLOW_CHUNK_SIZE)
              if not chunk:
                  break

              query_params = base_params
              query_params["flowCurrentChunkSize"] = len(chunk)
              query_params["flowChunkNumber"] = chunk_number

              self._upload_request(
                  query_params, upload_path, file_name, chunk
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

    def download(self, path, download_path):

        _client = client.get_instance()
        path_params = ["project", _client._project_id, "dataset", "download", "with_auth", path]
        query_params = {'type': 'DATASET'}

        with _client._send_request("GET", path_params, query_params=query_params, stream=True) as response:
            with open(download_path, "wb") as f:
                downloaded = 0
                file_size = response.headers.get('Content-Length')
                if not file_size:
                    print("Downloading file ...", end=" ")
                for chunk in response.iter_content(chunk_size=self.DEFAULT_FLOW_CHUNK_SIZE):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if file_size:
                        progress = round(downloaded / int(file_size) * 100, 3)
                        print("Progress: " + str(progress) + "%")
                if not file_size:
                    print("DONE")



    def get(self, remote_path):
        """Save model metadata to the model registry.

        :param remote_path: metadata object of feature group to be saved
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
        headers = {"content-type": "application/json"}
        return _client._send_request(
                "GET",
                path_params,
                headers=headers
            )


    def path_exists(self, remote_path):
        """Save model metadata to the model registry.

        :param remote_path: metadata object of feature group to be saved
        :type model_instance: Model
        :return: updated metadata object of the model
        :rtype: Model
        """
        try:
            self.get(remote_path)
            return True
        except RestAPIError:
            return False
    def list(self, remote_path, sort_by=None, limit=1000):
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
        query_params = {'action': 'listing', 'sort_by': sort_by, 'limit': limit}
        headers = {"content-type": "application/json"}
        return _client._send_request(
                "GET",
                path_params,
                headers=headers,
                query_params=query_params
            )

    def mkdir(self, remote_path):
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
        query_params = {'action': 'create', 'searchable': 'true', 'generate_readme': 'false', 'type': "DATASET"}
        headers = {"content-type": "application/json"}
        return _client._send_request(
                "POST",
                path_params,
                headers=headers,
                query_params=query_params
            )

    def rm(self, remote_path):
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
        return _client._send_request(
                "DELETE",
                path_params
            )

    def _path_exists(self, remote_path):
        """
        Check if path exists.

        Example usage:

        >>> from hops import dataset
        >>> dataset.path_exists("Projects/project_name/Resources/myremotefile.txt")

        Args:
            :remote_path: the path to the remote file or directory in the dataset

        Returns:
            True if path exists, False otherwise
        """
        try:
            self.get(remote_path)
            return True
        except Exception:
            return False

    def _archive(self, remote_path, destination_path=None, block=False, timeout=120, action='unzip'):
            """
            Create an archive (zip file) of a file or directory in a Hopsworks dataset.

            Args:
                :remote_path: the path to the remote file or directory in the dataset.
                :action: Allowed values are zip/unzip. Whether to compress/extract respectively.
                :block: whether this method should wait for the zipping process to complete before returning.
                :timeout: number of seconds to wait for the action to complete before returning.
            Returns:
                None
            """

            _client = client.get_instance()
            path_params = [
                "project",
                _client._project_id,
                "dataset",
                remote_path
            ]

            query_params = {'action': action}

            if destination_path is not None:
                query_params['destination_path'] = destination_path
                query_params['destination_type'] = 'DATASET'

            headers = {"content-type": "application/json"}

            print(_client._send_request(
                "POST",
                path_params,
                headers=headers,
                query_params=query_params
            ))

            if block is True:
                # Wait for zip file to appear. When it does, check that parent dir zipState is not set to CHOWNING
                count = 0
                while count < timeout:
                    if action is "zip":
                      zip_path = remote_path + ".zip"
                      # Get the status of the zipped file
                      if destination_path is None:
                          zip_exists = self._path_exists(zip_path)
                      else:
                          zip_exists = self._path_exists(destination_path + "/" + os.path.split(zip_path)[1])
                      print(zip_exists)
                      # Get the zipState of the directory being zipped
                      dir_status = self.get(remote_path)
                      print(dir_status)
                      zip_state = dir_status['zipState'] if 'zipState' in dir_status else None
                      print(zip_state)
                      if zip_exists and zip_state == 'NONE' :
                          return
                      else:
                          time.sleep(1)
                    elif action is "unzip":
                      # Get the status of the unzipped dir
                      unzipped_dir_exists = self._path_exists(remote_path[:-4])
                      # Get the zipState of the zip being extracted
                      dir_status = self.get(remote_path)
                      zip_state = dir_status['zipState'] if 'zipState' in dir_status else None
                      if unzipped_dir_exists and zip_state == 'NONE' :
                          return
                      else:
                          time.sleep(1)
                    count += 1
                raise Exception("Timeout of {} seconds exceeded while {} {}.".format(timeout, action, remote_path))

    def unzip(self, remote_path, block=False, timeout=120):
        """
        Extract the dir or file in Hopsworks, specified by the remote_path.

        Example usage:

        >>> from hops import dataset
        >>> dataset.extract("Projects/project_name/Resources/myremotefile.zip")

        Args:
            :remote_path: the path to the remote file or directory in the dataset
            :project_name: whether this method should wait for the zipping process to complete before returning.
            :block: whether to wait for the extraction to complete or not.
            :timeout: number of seconds to wait for the extraction to complete before returning.

        Returns:
            None
        """
        self._archive(remote_path, block=block, timeout=timeout, action='unzip')

    def zip(self, remote_path, destination_path=None, block=False, timeout=120):
        """
        Extract the dir or file in Hopsworks, specified by the remote_path.

        Example usage:

        >>> from hops import dataset
        >>> dataset.extract("Projects/project_name/Resources/myremotefile.zip")

        Args:
            :remote_path: the path to the remote file or directory in the dataset
            :project_name: whether this method should wait for the zipping process to complete before returning.
            :block: whether to wait for the extraction to complete or not.
            :timeout: number of seconds to wait for the extraction to complete before returning.

        Returns:
            None
        """
        self._archive(remote_path, destination_path=destination_path, block=block, timeout=timeout, action='zip')

    def move(self, source_path, destination_path):
        """
        Create an archive (zip file) of a file or directory in a Hopsworks dataset.

        Args:
            :remote_path: the path to the remote file or directory in the dataset.
            :action: Allowed values are zip/unzip. Whether to compress/extract respectively.
            :block: whether this method should wait for the zipping process to complete before returning.
            :timeout: number of seconds to wait for the action to complete before returning.
        Returns:
            None
        """

        _client = client.get_instance()
        path_params = [
            "project",
            _client._project_id,
            "dataset",
            source_path
        ]

        query_params = {'action': 'move', 'destination_path': destination_path}
        headers = {"content-type": "application/json"}

        _client._send_request(
            "POST",
            path_params,
            headers=headers,
            query_params=query_params
        )
