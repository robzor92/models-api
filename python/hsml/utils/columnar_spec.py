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

from hsml.utils.column import Column
import pandas

class ColumnarSpec:
    """Metadata object representing a model signature for a model."""

    def __init__(
            self,
            pandas_obj: None
    ):

        self._columns = self._convert_pandas_to_signature(pandas_obj)

    def _convert_pandas_to_signature(self, columnar_obj):
        columns = []
        if isinstance(columnar_obj, pandas.DataFrame):
            pandas_columns = columnar_obj.columns
            pandas_data_types = columnar_obj.dtypes
            columns = []
            for name in pandas_columns:
                columns.append(Column(name=name, data_type=str(pandas_data_types[name])))
        elif isinstance(columnar_obj, pandas.Series):
            columns.append(Column(name='series', data_type=str(columnar_obj.dtypes)))
        return columns

    def _convert_spark_to_signature(self, spark_df):
        pass
        #TODO implement Spark DF to signature

    def to_dict(self):
        return {
            "columns": self._columns
        }

    @property
    def columns(self):
        """columns of the model."""
        return self._columns

    @columns.setter
    def columns(self, columns):
        self._columns = columns
