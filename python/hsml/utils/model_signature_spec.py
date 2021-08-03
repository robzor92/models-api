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
            self.columnar_spec = self._convert_columnar_to_signature(data)
        else:
            self.tensor_spec = self._convert_tensor_to_signature(data)


    def _convert_columnar_to_signature(self, data):
        return ColumnarSpec(data)

    def _convert_tensor_to_signature(self, data):
        return TensorSpec(data)

    def to_dict(self):
        sig_dict = {}
        if hasattr(self, "columnarSpec"):
            sig_dict["columnarSpec"] = self.columnar_spec
        if hasattr(self, "tensorSpec"):
            sig_dict["tensorSpec"] = self.tensor_spec
        return sig_dict
