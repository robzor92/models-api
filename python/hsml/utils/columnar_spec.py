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

class ColumnarSpec:
    """Metadata object representing a model signature for a model."""

    def __init__(
            self,
            signature_array: None
    ):

        self._columns = self._convert_to_columns(signature_array)

    def _convert_pandas_to_signature(self, data):

        columns = []
        for name in data:
            columns.append(Column(name=name, dataType=data[name]))

        return ColumnarSpec(signature_arr)

    def to_dict(self):
        return {
            "columnarSpec": self._columns
        }

    @property
    def columns(self):
        """columns of the model."""
        return self._columns

    @columns.setter
    def columns(self, columns):
        self._icolumns = columns
