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

from hsfs import client
from hsfs import model

class ModelsApi:

    def __init__(self):

    def save(self, model_instance):
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
            "models"
        ]
        headers = {"content-type": "application/json"}
        return model_instance.update_from_response_json(
            _client._send_request(
                "POST",
                path_params,
                headers=headers,
                data=model_instance.json(),
            ),
        )

    def get(self, name, version):
        """Get the metadata of a model with a certain name and version.

        :param name: name of the model
        :type name: str
        :param version: version of the model
        :type version: int
        :return: model metadata object
        :rtype: Model
        """
        _client = client.get_instance()
        path_params = [
            "project",
            _client._project_id,
            "models",
            name
        ]
        query_params = {"version": version}
        model_json = _client._send_request("GET", path_params, query_params)[0]
        return model.Model.from_response_json(model_json)

    def delete(self, model_instance):
        """Delete the model and metadata.

        :param model_instance: metadata object of model to delete
        :type model_instance: Model
        """
        _client = client.get_instance()
        path_params = [
            "project",
            _client._project_id,
            "models",
            model_instance
        ]
        _client._send_request("DELETE", path_params)

    def update_metadata(
        self,
        feature_group_instance,
        feature_group_copy,
        query_parameter,
        query_parameter_value=True,
    ):
        """Update the metadata of a feature group.

        This only updates description and schema/features. The
        `feature_group_copy` is the metadata object sent to the backend, while
        `feature_group_instance` is the user object, which is only updated
        after a successful REST call.

        # Arguments
            feature_group_instance: FeatureGroup. User metadata object of the
                feature group.
            feature_group_copy: FeatureGroup. Metadata object of the feature
                group with the information to be updated.
            query_parameter: str. Query parameter that controls which information is updated. E.g. "updateMetadata",
                or "validationType".
            query_parameter_value: Str. Value of the query_parameter.

        # Returns
            FeatureGroup. The updated feature group metadata object.
        """
        _client = client.get_instance()
        path_params = [
            "project",
            _client._project_id,
            "featurestores",
            self._feature_store_id,
            "featuregroups",
            feature_group_instance.id,
        ]
        headers = {"content-type": "application/json"}
        query_params = {query_parameter: query_parameter_value}
        return feature_group_instance.update_from_response_json(
            _client._send_request(
                "PUT",
                path_params,
                query_params,
                headers=headers,
                data=feature_group_copy.json(),
            ),
        )