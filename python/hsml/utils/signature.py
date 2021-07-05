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
import numpy
import pandas

class Signature:
    """Metadata object representing a model signature for a model."""

    def __init__(
            self,
            inputs: Optional[Union[dict, list, pandas.core.frame.DataFrame, numpy.ndarray]] = None,
            predictions: Optional[Union[dict, list, pandas.core.frame.DataFrame, numpy.ndarray]] = None
        ):

        if inputs is not None:
            self._inputs = self._convert_to_signature(inputs)

        if predictions is not None:
            self._predictions = self._convert_to_signature(predictions)

    def _convert_to_signature(self, df):

        columns = df.columns
        datatypes = df.dtypes

        signature_arr = []

        for column in columns:
            signature_arr.append([{column: datatypes[column]}])

        return signature_arr

    def to_dict(self):
        return {
            "inputs": self._inputs,
            "predictions": self._predictions
        }

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

