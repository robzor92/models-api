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

import pydoop.hdfs as hdfs
import os

class NativeHdfsApi:

    def __init__(self):
        pass

    def exists(self, hdfs_path):
        return hdfs.path.exists(hdfs_path)

    def project_path(self):
        project = os.environ["HADOOP_USER_NAME"].split("__")[0]
        return hdfs.path.abspath("/Projects/" + project + "/")

    def chmod(self, hdfs_path, mode):
        return hdfs.chmod(hdfs_path, mode)

    def mkdir(self, path):
        return hdfs.mkdir(path)