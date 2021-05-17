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

import re
import json

from datetime import datetime

class ModelRegistryEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return o.to_dict()
        except AttributeError:
            return super().default(o)

def setup_pydoop():
    # Import Pydoop only here, so it doesn't trigger if the execution environment
    # does not support Pydoop. E.g. Sagemaker
    from pydoop import hdfs

    # Create a subclass that replaces the check on the hdfs scheme to allow hopsfs as well.
    class _HopsFSPathSplitter(hdfs.path._HdfsPathSplitter):
        @classmethod
        def split(cls, hdfs_path, user):
            if not hdfs_path:
                cls.raise_bad_path(hdfs_path, "empty")
            scheme, netloc, path = cls.parse(hdfs_path)
            if not scheme:
                scheme = "file" if hdfs.fs.default_is_local() else "hdfs"
            if scheme == "hdfs" or scheme == "hopsfs":
                if not path:
                    cls.raise_bad_path(hdfs_path, "path part is empty")
                if ":" in path:
                    cls.raise_bad_path(hdfs_path, "':' not allowed outside netloc part")
                hostname, port = cls.split_netloc(netloc)
                if not path.startswith("/"):
                    path = "/user/%s/%s" % (user, path)
            elif scheme == "file":
                hostname, port, path = "", 0, netloc + path
            else:
                cls.raise_bad_path(hdfs_path, "unsupported scheme %r" % scheme)
            return hostname, port, path

    # Monkey patch the class to use the one defined above.
    hdfs.path._HdfsPathSplitter = _HopsFSPathSplitter