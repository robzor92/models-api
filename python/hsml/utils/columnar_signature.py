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
from typing import Dict, List, Union, Optional
import pandas
try:
    import pyspark
except:
    pass

class ColumnarSignature:
    """Metadata object representing a columnar signature for a model."""

    def __init__(
            self,
            columnar_obj: Optional[Union[pandas.core.frame.DataFrame, pyspark.sql.dataframe.DataFrame]] = None
    ):
         if isinstance(columnar_obj, pyspark.sql.dataframe.DataFrame):
             self.columns = self._convert_spark_to_signature(columnar_obj)
         else:
             self.columns = self._convert_pandas_to_signature(columnar_obj)

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
        columns = []
        if isinstance(spark_df, pyspark.sql.dataframe.DataFrame):
            types = spark_df.dtypes
            for dtype in types:
                name, dtype = dtype
                columns.append(Column(name=name, data_type=str(dtype)))
        return columns

    def to_dict(self):
        return {
            "columns": self.columns
        }