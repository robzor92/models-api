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
from hsml.utils.tensor_spec import TensorSpec
import numpy
import pandas

class ModelSignatureSpec:
    """Metadata object representing a model signature for a model."""

    def __init__(
            self,
            data: Optional[Union[dict, list, pandas.core.frame.DataFrame, numpy.ndarray]] = None,
    ):

        if isinstance(data, pandas.Series) or isinstance(data, pandas.DataFrame):
            self._columnar_spec = self._convert_columnar_to_signature(data)
        else:
            self._tensor_spec = None


    def _convert_columnar_to_signature(self, data):
        return ColumnarSpec(data)

    def _convert_tensor_to_signature(self, data):
        return TensorSpec(data)

    def to_dict(self):
        sig_dict = {}
        if self._columnar_spec is not None:
            sig_dict["columnarSpec"] = self._columnar_spec
        if self._tensor_spec is not None:
            sig_dict["tensorSpec"] = self._tensor_spec
        return sig_dict

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

