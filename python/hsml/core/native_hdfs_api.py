
import pydoop.hdfs as hdfs
import os

class NativeHdfsApi:

    def __init__(self):
        pass

    def exists(self, hdfs_path):
        return hdfs.path.exists(hdfs_path)

    def project_path(self):
        project = os.environ["HOPSWORKS_PROJECT_NAME"]
        return hdfs.path.abspath("/Projects/" + project + "/")

    def chmod(self, hdfs_path, mode):
        return hdfs.chmod(hdfs_path, mode)

