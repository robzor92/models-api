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

from hsmr.core import models_api


class ModelsEngine:
    def __init__(self, model_registry_id):
        """Models engine.

        :param feature_store_id: id of the respective featurestore
        :type feature_store_id: int
        """
        self.model_registry_id = model_registry_id
        self.models_api = models_api.ModelsApi(model_registry_id)

    def save(self, model):
        print("expectation.rules[0].to_dict()" + str(expectation.rules[0].to_dict()))
        self._expectations_api.create(expectation)
