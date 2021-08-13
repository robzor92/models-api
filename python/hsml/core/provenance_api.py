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

from hsml import client, util

class ProvenanceApi:

    def get_model_td(self, model_id):
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
            "provenance",
            "links"
        ]
        query_params = {'only_apps': 'true', 'full_link': 'true', 'filter_by': ['OUT_TYPE:MODEL','IN_TYPE:TRAINING_DATASET','OUT_ARTIFACT:{}'.format(model_id)]}
        headers = {"content-type": "application/json"}
        return _client._send_request(
            "GET",
            path_params,
            headers=headers,
            query_params=query_params
        )