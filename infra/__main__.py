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

import sys

import pulumi
from pulumi import Output

import pulumi_datarobot as datarobot

import datarobot as dr
import yaml

sys.path.append("..")

from infra import (
    settings_main,
)
from infra.common.papermill import run_notebook
from infra.settings_deployment import (
    deployment_args,
    retraining_policy_settings
)

from infra.common.schema_retraining import (
    Action,
    CVMethod,
    FeatureListStrategy,
    ModelSelectionStrategy,
    ProjectOptionsStrategy,
    TriggerType,
)

from infra.settings_main import model_training_nb_path, model_training_output_path,project_name, challenger_model_output_path

from starter.i18n import LocaleSettings
from starter.resources import (
    deployment_env_name,
    scoring_dataset_env_name,
)
from starter.schema import AppSettings
from starter.make_prediction import prediction_and_upload_actual
from starter.make_challenger import train_and_create_challangers


LocaleSettings().setup_locale()

if not model_training_output_path.exists():
    pulumi.info("Executing model training notebook...")
    run_notebook(model_training_nb_path)
else:
    pulumi.info(
        f"Using existing model training outputs in '{model_training_output_path}'"
    )
with open(model_training_output_path) as f:
    model_training_output = AppSettings(**yaml.safe_load(f))

prediction_environment = datarobot.PredictionEnvironment(
    **settings_main.prediction_environment_args,
)


deployment = datarobot.Deployment(
    prediction_environment_id=prediction_environment.id,
    registered_model_version_id=model_training_output.registered_model_version_id,
    **deployment_args.model_dump(),
    use_case_ids=[model_training_output.use_case_id],
)
# ------ 再学習用のポリシーを作成 -------
retraining_policy = datarobot.DeploymentRetrainingPolicy(
        deployment_id=deployment.id,
        **retraining_policy_settings.model_dump(),
    )

retraining_policy_datadrift = datarobot.DeploymentRetrainingPolicy(
        f"Retrain on DataDrift Decline [{project_name}]",
        deployment_id=deployment.id,
        description="DataDrift Detection",
        action=Action.CreateChallenger,
        autopilot_options={
            "blend_best_models": False,
            "mode": dr.enums.AUTOPILOT_MODE.QUICK,
            "run_leakage_removed_feature_list": True,
            "scoring_code_only": False,
            "shap_only_mode": False,
        },
        project_options_strategy=ProjectOptionsStrategy.SameAsChampion,
        feature_list_strategy=FeatureListStrategy.InformativeFeatures,
        model_selection_strategy=ModelSelectionStrategy.AutopilotRecommended,
        name="DataDrift",
        project_options={
            "cv_method": CVMethod.RandomCV,
            "holdout_pct": None,
            "metric": dr.enums.ACCURACY_METRIC.LOGLOSS,
            "reps": None,
            "validation_pct": None,
            "validation_type": dr.enums.VALIDATION_TYPE.CV,
        },
        trigger={
            "status_declines_to_failing": True,
            "status_declines_to_warning": True,
            "status_still_in_decline": False,
            "type":TriggerType.data_drift_decline,
        },
)

custom_model = datarobot.CustomModel(f"Custom Model [{project_name}]",
                                              base_environment_id="5e8c889607389fe0f466c72d",
                                              base_environment_version_id="67d1385fa03d158140e0baa1",
                                              #memory_mb=512,
                                              target_name="ブリードアウト",
                                              description=f"Custom Model [{project_name}]",
                                              name=f"Custom Model [{project_name}]",
                                              target_type="Binary",
                                              negative_class_label="False",
                                              positive_class_label="True",
                                              prediction_threshold=0.5,
                                              use_case_ids=[model_training_output.use_case_id],
                                              training_dataset_id=model_training_output.training_dataset_id,
                                              folder_path="../assets/custom_model")

example_registered_model = datarobot.RegisteredModel(f"Registered Custom Model [{project_name}]",
                                                     custom_model_version_id=custom_model.version_id,
                                                     version_name=model_training_output.registered_model_name,
                                                     #name=model_training_output.registered_model_name,
                                                     use_case_ids=[model_training_output.use_case_id],
                                                     description="Description for the example registered model")

if not challenger_model_output_path.exists():

    
    pulumi.info("Making prediction and set actual...")
    Output.all(deployment.id).apply(lambda args: prediction_and_upload_actual(f"{args[0]}"))
    pulumi.info("Executing challanger traning and register...")
    
    Output.all(deployment.id, prediction_environment.id) \
        .apply(lambda args: train_and_create_challangers(f"{args[0]}", f"{args[1]}"))
else:
    pulumi.info(
        f"Using existing model training outputs in '{challenger_model_output_path}'"
    )
    
pulumi.export(scoring_dataset_env_name, model_training_output.training_dataset_id)
pulumi.export(deployment_env_name, deployment.id)