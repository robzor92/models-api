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

class Signature(object):

    def __init__(
            self,
            inputs: Optional[list] = None,
            predictions: Optional[list] = None
        ):

        if inputs is not None:
            self._input = convert_to_signature(inputs)

        if predictions is not None:
            self._predictions = convert_to_signature(predictions)

    def convert_to_signature(df):
    
        columns = df.columns
        datatypes = df.dtypes

        signature_arr = []

        for column in columns:
            signature_arr.append([{column: datatypes[column]}]

        return signature_arr

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

