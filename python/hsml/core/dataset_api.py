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
import json
from hsml.client.exceptions import RestAPIError
import time

from hsml import client, tag


class DatasetApi:
    def __init__(self):
        pass

    DEFAULT_FLOW_CHUNK_SIZE = 1048576

    def upload(self, local_abs_path, upload_path):

        size = os.path.getsize(local_abs_path)

        _, file_name = os.path.split(local_abs_path)

        num_chunks = math.ceil(size / self.DEFAULT_FLOW_CHUNK_SIZE)

        base_params = self._get_flow_base_params(file_name, num_chunks, size)

        chunk_number = 1
        with open(local_abs_path, "rb") as f:
            while True:
                chunk = f.read(self.DEFAULT_FLOW_CHUNK_SIZE)
                if not chunk:
                    break

                query_params = base_params
                query_params["flowCurrentChunkSize"] = len(chunk)
                query_params["flowChunkNumber"] = chunk_number

                self._upload_request(query_params, upload_path, file_name, chunk)

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
        path_params = [
            "project",
            _client._project_id,
            "dataset",
            "download",
            "with_auth",
            path,
        ]
        query_params = {"type": "DATASET"}

        with _client._send_request(
            "GET", path_params, query_params=query_params, stream=True
        ) as response:
            with open(download_path, "wb") as f:
                downloaded = 0
                file_size = response.headers.get("Content-Length")
                if not file_size:
                    print("Downloading file ...", end=" ")
                for chunk in response.iter_content(
                    chunk_size=self.DEFAULT_FLOW_CHUNK_SIZE
                ):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if file_size:
                        progress = round(downloaded / int(file_size) * 100, 3)
                        print("Progress: " + str(progress) + "%")
                if not file_size:
                    print("Download complete")

    def get(self, remote_path):
        """Save model metadata to the model registry.

        :param remote_path: metadata object of feature group to be saved
        :type model_instance: Model
        :return: updated metadata object of the model
        :rtype: Model
        """
        _client = client.get_instance()
        path_params = ["project", _client._project_id, "dataset", remote_path]
        headers = {"content-type": "application/json"}
        return _client._send_request("GET", path_params, headers=headers)

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
        path_params = ["project", _client._project_id, "dataset", remote_path]
        query_params = {"action": "listing", "sort_by": sort_by, "limit": limit}
        headers = {"content-type": "application/json"}
        return _client._send_request(
            "GET", path_params, headers=headers, query_params=query_params
        )

    def chmod(self, remote_path, permissions):
        """Save model metadata to the model registry.

        :param model_instance: metadata object of feature group to be saved
        :type model_instance: Model
        :return: updated metadata object of the model
        :rtype: Model
        """
        _client = client.get_instance()
        path_params = ["project", _client._project_id, "dataset", remote_path]
        headers = {"content-type": "application/json"}
        query_params = {"action": "PERMISSION", "permissions": permissions}
        return _client._send_request(
            "PUT", path_params, headers=headers, query_params=query_params
        )

    def mkdir(self, remote_path):
        """Save model metadata to the model registry.

        :param model_instance: metadata object of feature group to be saved
        :type model_instance: Model
        :return: updated metadata object of the model
        :rtype: Model
        """
        _client = client.get_instance()
        path_params = ["project", _client._project_id, "dataset", remote_path]
        query_params = {
            "action": "create",
            "searchable": "true",
            "generate_readme": "false",
            "type": "DATASET",
        }
        headers = {"content-type": "application/json"}
        return _client._send_request(
            "POST", path_params, headers=headers, query_params=query_params
        )

    def rm(self, remote_path):
        """Save model metadata to the model registry.

        :param model_instance: metadata object of feature group to be saved
        :type model_instance: Model
        :return: updated metadata object of the model
        :rtype: Model
        """
        _client = client.get_instance()
        path_params = ["project", _client._project_id, "dataset", remote_path]
        return _client._send_request("DELETE", path_params)

    def _path_exists(self, remote_path):
        """
        Check if path exists.

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

    def _archive(
        self,
        remote_path,
        destination_path=None,
        block=False,
        timeout=120,
        action="unzip",
    ):
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
        path_params = ["project", _client._project_id, "dataset", remote_path]

        query_params = {"action": action}

        if destination_path is not None:
            query_params["destination_path"] = destination_path
            query_params["destination_type"] = "DATASET"

        headers = {"content-type": "application/json"}

        _client._send_request(
            "POST", path_params, headers=headers, query_params=query_params
        )

        if block is True:
            # Wait for zip file to appear. When it does, check that parent dir zipState is not set to CHOWNING
            count = 0
            while count < timeout:
                if action == "zip":
                    zip_path = remote_path + ".zip"
                    # Get the status of the zipped file
                    if destination_path is None:
                        zip_exists = self._path_exists(zip_path)
                    else:
                        zip_exists = self._path_exists(
                            destination_path + "/" + os.path.split(zip_path)[1]
                        )
                    # Get the zipState of the directory being zipped
                    dir_status = self.get(remote_path)
                    zip_state = (
                        dir_status["zipState"] if "zipState" in dir_status else None
                    )
                    if zip_exists and zip_state == "NONE":
                        return
                    else:
                        time.sleep(1)
                elif action == "unzip":
                    # Get the status of the unzipped dir
                    unzipped_dir_exists = self._path_exists(remote_path[:-4])
                    # Get the zipState of the zip being extracted
                    dir_status = self.get(remote_path)
                    zip_state = (
                        dir_status["zipState"] if "zipState" in dir_status else None
                    )
                    if unzipped_dir_exists and zip_state == "NONE":
                        return
                    else:
                        time.sleep(1)
                count += 1
            raise Exception(
                "Timeout of {} seconds exceeded while {} {}.".format(
                    timeout, action, remote_path
                )
            )

    def unzip(self, remote_path, block=False, timeout=120):
        """
        Extract the dir or file in Hopsworks, specified by the remote_path.

        Args:
            :remote_path: the path to the remote file or directory in the dataset
            :project_name: whether this method should wait for the zipping process to complete before returning.
            :block: whether to wait for the extraction to complete or not.
            :timeout: number of seconds to wait for the extraction to complete before returning.

        Returns:
            None
        """
        self._archive(remote_path, block=block, timeout=timeout, action="unzip")

    def zip(self, remote_path, destination_path=None, block=False, timeout=120):
        """
        Extract the dir or file in Hopsworks, specified by the remote_path.


        Args:
            :remote_path: the path to the remote file or directory in the dataset
            :project_name: whether this method should wait for the zipping process to complete before returning.
            :block: whether to wait for the extraction to complete or not.
            :timeout: number of seconds to wait for the extraction to complete before returning.

        Returns:
            None
        """
        self._archive(
            remote_path,
            destination_path=destination_path,
            block=block,
            timeout=timeout,
            action="zip",
        )

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
        path_params = ["project", _client._project_id, "dataset", source_path]

        query_params = {"action": "move", "destination_path": destination_path}
        headers = {"content-type": "application/json"}

        _client._send_request(
            "POST", path_params, headers=headers, query_params=query_params
        )

    def add(self, path, name, value):
        """Attach a name/value tag to a training dataset or feature group.

        A tag consists of a name/value pair. Tag names are unique identifiers.
        The value of a tag can be any valid json - primitives, arrays or json objects.

        :param metadata_instance: metadata object of the instance to add the
            tag for
        :type metadata_instance: TrainingDataset, FeatureGroup
        :param name: name of the tag to be added
        :type name: str
        :param value: value of the tag to be added
        :type value: str
        """
        _client = client.get_instance()
        path_params = [
            "project",
            _client._project_id,
            "dataset",
            "tags",
            "schema",
            name,
            path,
        ]
        headers = {"content-type": "application/json"}
        json_value = json.dumps(value)
        _client._send_request("PUT", path_params, headers=headers, data=json_value)

    def delete(self, path, name):
        """Delete a tag.

        Tag names are unique identifiers.

        :param metadata_instance: metadata object of training dataset
            to delete the tag for
        :type metadata_instance: TrainingDataset, FeatureGroup
        :param name: name of the tag to be removed
        :type name: str
        """
        _client = client.get_instance()
        path_params = [
            "project",
            _client._project_id,
            "dataset",
            "tags",
            "schema",
            name,
            path,
        ]
        _client._send_request("DELETE", path_params)

    def get_tags(self, path, name: str = None):
        """Get the tags.

        Gets all tags if no tag name is specified.

        :param metadata_instance: metadata object of training dataset
            to get the tags for
        :type metadata_instance: TrainingDataset, FeatureGroup
        :param name: tag name
        :type name: str
        :return: dict of tag name/values
        :rtype: dict
        """
        _client = client.get_instance()
        path_params = [
            "project",
            _client._project_id,
            "dataset",
            "tags",
        ]

        if name is not None:
            path_params.append("schema")
            path_params.append(name)
        else:
            path_params.append("all")

        path_params.append(path)

        return {
            tag._name: json.loads(tag._value)
            for tag in tag.Tag.from_response_json(
                _client._send_request("GET", path_params)
            )
        }
