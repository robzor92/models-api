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

import json
import shutil
import os
import datetime

from json import JSONEncoder

class VersionWarning(Warning):
    pass

class MLEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return o.to_dict()
        except AttributeError:
            return super().default(o)


class NumpyEncoder(JSONEncoder):
    """ Special json encoder for numpy types.
    Note that some numpy types doesn't have native python equivalence,
    hence json.dumps will raise TypeError.
    In this case, you'll need to convert your numpy types into its closest python equivalence.
    """

    def try_convert(self, o):
        import numpy as np
        import pandas as pd
        import base64

        def encode_binary(x):
            return base64.encodebytes(x).decode("ascii")

        if isinstance(o, np.ndarray):
            if o.dtype == np.object:
                return [self.try_convert(x)[0] for x in o.tolist()]
            elif o.dtype == np.bytes_:
                return np.vectorize(encode_binary)(o), True
            else:
                return o.tolist(), True

        if isinstance(o, np.generic):
            return o.item(), True
        if isinstance(o, bytes) or isinstance(o, bytearray):
            return encode_binary(o), True
        if isinstance(o, np.datetime64):
            return np.datetime_as_string(o), True
        if isinstance(o, (pd.Timestamp, datetime.date)):
            return o.isoformat(), True
        return o, False

    def default(self, o):  # pylint: disable=E0202
        res, converted = self.try_convert(o)
        if converted:
            return res
        else:
            return super().default(o)

    def _is_scalar(self, x):
        return np.isscalar(x) or x is None

    def _is_ndarray(self, x):
        return isinstance(x, np.ndarray) or (isinstance(x, dict) and all([isinstance(ary, np.ndarray) for ary in x.values()]))

    def _handle_tensor_input(self, input_tensor: Union[np.ndarray, dict]):
        if isinstance(input_tensor, dict):
            result = {}
            for name in input_tensor.keys():
                result[name] = input_tensor[name].tolist()
            return {"data": result}
        else:
            return {"data": input_tensor.tolist()}

    def input_example_to_json(input_example):
        if self._is_ndarray(input_example):
            return self._handle_tensor_input(input_example)
        else:
            return self._handle_dataframe_input(input_example)

    def _handle_dataframe_input(self, input_ex):
        if isinstance(input_ex, dict):
            if all([self._is_scalar(x) for x in input_ex.values()]):
                input_ex = pd.DataFrame([input_ex])
            else:
                raise TypeError(
                    "Data in the dictionary must be scalar or of type numpy.ndarray"
                )
        elif isinstance(input_ex, list):
            for i, x in enumerate(input_ex):
                if isinstance(x, np.ndarray) and len(x.shape) > 1:
                    raise TensorsNotSupportedException(
                        "Row '{0}' has shape {1}".format(i, x.shape)
                    )
            if all([self._is_scalar(x) for x in input_ex]):
                input_ex = pd.DataFrame([input_ex], columns=range(len(input_ex)))
            else:
                input_ex = pd.DataFrame(input_ex)
        elif not isinstance(input_ex, pd.DataFrame):
            try:
                import pyspark.sql.dataframe

                if isinstance(input_example, pyspark.sql.dataframe.DataFrame):
                    raise Exception(
                        "Examples can not be provided as Spark Dataframe. "
                        "Please make sure your example is of a small size and "
                        "turn it into a pandas DataFrame."
                    )
            except ImportError:
                pass
            raise TypeError(
                "Unexpected type of input_example. Expected one of "
                "(pandas.DataFrame, numpy.ndarray, dict, list), "
                "got {}".format(type(input_example))
            )
        result = input_ex.to_dict(orient="split")
        # Do not include row index
        del result["index"]
        if all(input_ex.columns == range(len(input_ex.columns))):
            # No need to write default column index out
            del result["columns"]
        return result


    def read_input_example(self, model_instance, input_example_path):
        try:
            tmp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
            self._dataset_api.download(input_example_path, tmp_dir.name + '/inputs.json')
            with open(tmp_dir.name + '/inputs.json', 'rb') as f:
                return json.loads(f.read())
        finally:
            if tmp_dir is not None and os.path.exists(tmp_dir.name):
                tmp_dir.cleanup()

def zip(zip_out_dir, dir_to_zip):
    return shutil.make_archive(zip_out_dir + "/archive", 'zip', dir_to_zip)