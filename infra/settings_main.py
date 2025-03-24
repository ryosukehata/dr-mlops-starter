# Copyright 2024 DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pathlib import Path

from infra.common.globals import GlobalPredictionEnvironmentPlatforms

from .common.schema import (
    PredictionEnvironmentArgs,
    UseCaseArgs,
)
from .common.stack import get_stack

project_name = get_stack()

prediction_environment_args = PredictionEnvironmentArgs(
    resource_name=f"Predictive AI MLOps Starter Prediction Environment [{project_name}]",
    platform=GlobalPredictionEnvironmentPlatforms.DATAROBOT_SERVERLESS,
).model_dump(mode="json", exclude_none=True)


use_case_args = UseCaseArgs(
    resource_name=f"Predictive AI MLOps  Starter Use Case [{project_name}]",
    description="Use Case for Predictive AI MLOps Starter application",
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.absolute()

outputs_path_str = str(PROJECT_ROOT / "outputs")
runtime_parameters_spec_template = "metadata.yaml.jinja"
runtime_parameters_spec = "metadata.yaml"

model_training_nb_name = "train_model.ipynb"
model_training_nb_path = PROJECT_ROOT / "notebooks" / model_training_nb_name
model_training_nb_output_name = "train_model_output.yaml"
model_training_output_name = f"train_model_output.{project_name}.yaml"
model_training_output_path_str = f"{outputs_path_str}/{model_training_output_name}"
model_training_output_path = Path(model_training_output_path_str)

challenger_model_output_name = f"challenger_model_output.{project_name}.yaml"
challenger_model_output_path_str = f"{outputs_path_str}/{challenger_model_output_name}"
challenger_model_output_path = Path(challenger_model_output_path_str)