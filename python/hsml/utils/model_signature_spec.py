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
from hsml.utils.columnar_spec import ColumnarSpec
import numpy
import pandas as pd

class ModelSignatureSpec:
    """Metadata object representing a model signature for a model."""

    def __init__(
            self,
            data: Optional[Union[dict, list, pandas.core.frame.DataFrame, numpy.ndarray]] = None,
    ):

        if isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
            self._columnar_spec = self._convert_pandas_to_signature(data)
        else:
            self._tensor_spec = None

    def _convert_pandas_to_signature(self, data):
        return ColumnarSpec(data)

    def to_dict(self):
        return {
            "columnarSpec": self._columnar_spec,
            "tensorSpec": self._tensor_spec
        }

    @property
    def columnar_spec(self):
        """columnar_spec of the model."""
        return self._columnar_spec

    @columnar_spec.setter
    def columnar_spec(self, columnar_spec):
        self._columnar_spec = columnar_spec

    @property
    def tensor_spec(self):
        """tensor_spec of the model."""
        return self._tensor_spec

    @tensor_spec.setter
    def tensor_spec(self, tensor_spec):
        self._tensor_spec = tensor_spec

