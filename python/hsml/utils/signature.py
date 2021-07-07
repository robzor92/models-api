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

from typing import Dict, List, Union, Optional
import json
from hsml import util
import numpy
import pandas

from hsml.utils.model_signature_spec import ModelSignatureSpec

class Signature:
    """Metadata object representing a model signature for a model."""

    def __init__(
            self,
            inputs: Optional[Union[dict, list, pandas.core.frame.DataFrame, numpy.ndarray]] = None,
            predictions: Optional[Union[dict, list, pandas.core.frame.DataFrame, numpy.ndarray]] = None
        ):

        self._inputs = self._convert_to_signature(inputs)
        self._predictions = self._convert_to_signature(predictions)

    def _convert_to_signature(self, data):
        return ModelSignatureSpec(data)

    def to_dict(self):
        return {
            "inputs": self._inputs,
            "predictions": self._predictions
        }

    def json(self):
        return json.dumps(self, cls=util.MLEncoder)

    def update_from_response_json(self, json_dict):
        json_decamelized = humps.decamelize(json_dict)
        _ = json_decamelized.pop("type")
        # here we lose the information that the user set, e.g. write_options
        self.__init__(**json_decamelized)
        return self

    @property
    def inputs(self):
        """inputs of the model."""
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @property
    def predictions(self):
        """predictions of the model."""
        return self._predictions

    @predictions.setter
    def predictions(self, predictions):
        self._predictions = predictions

