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

from hsml.model import Model


class Model(Model):
    """Metadata object representing a model in the Model Registry."""

    def __init__(
        self,
        id,
        name,
        version=None,
        created=None,
        environment=None,
        description=None,
        metrics=None,
        signature=None,
        training_dataset=None,
        input_example=None,
    ):
        super().__init__(
            id,
            name,
            version=version,
            created=created,
            environment=environment,
            description=description,
            metrics=metrics,
            input_example=input_example,
            signature=signature,
            training_dataset=training_dataset,
        )
