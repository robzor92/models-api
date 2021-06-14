from hsml import client
from hsml.model_registry import ModelRegistry


class ModelRegistryApi:
    def __init__(self):
        pass

    def get(self):
        """Get model registry store with specific id or name.

        :return: the model registry metadata
        :rtype: ModelRegistry
        """
        _client = client.get_instance()
        path_params = ["project", _client._project_id, "models"]
        return ModelRegistry.from_response_json(
            _client._send_request("GET", path_params)
        )
