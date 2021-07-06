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

from hsml.utils.tensor import Tensor
import numpy

class TensorSpec:
    """Metadata object representing a model signature for a model."""

    def __init__(
            self,
            tensor_obj: None
    ):
        data_type, shape = self._get_tensor_spec(tensor_obj)

        self._data_type = data_type
        self._shape = shape

    def _get_tensor_spec(self, tensor_obj):
        return 1, 2

    def to_dict(self):
        return {
            "shape": self._shape,
            "dataType": self._data_type
        }

    @property
    def shape(self):
        """shape of the model."""
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape

    @property
    def data_type(self):
        """data_type of the model."""
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        self._data_type = data_type

