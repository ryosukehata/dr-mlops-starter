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


import datarobot as dr
import pulumi_datarobot as datarobot

from .common.schema import (
    DeploymentArgs,
    DeploymentRetrainingPolicyArgs
)

from infra.common.schema_retraining import (
    Action,
    AutopilotOptions,
    CVMethod,
    FeatureListStrategy,
    ModelSelectionStrategy,
    ProjectOptions,
    ProjectOptionsStrategy,
    Schedule,
    Trigger,
    TriggerType,
)

from .settings_main import project_name

date_col = "date_col" 
datetime_format = "%Y-%m-%d"
association_id = "ロット番号"  # 実績と紐付くためのカラム
segment_analysis_attributes = ["塗布長"]


deployment_args = DeploymentArgs(
    resource_name=f"Predictive AI MLOps Starter Deployment [{project_name}]",
    label=f"Predictive AI MLOps Starter Deployment [{project_name}]",
    predictions_settings=(
        datarobot.DeploymentPredictionsSettingsArgs(min_computes=0, max_computes=1)
    ),
    drift_tracking_settings=datarobot.DeploymentDriftTrackingSettingsArgs(
            feature_drift_enabled=True,
            target_drift_enabled=True,
    ),
    association_id_settings=datarobot.DeploymentAssociationIdSettingsArgs(
            auto_generate_id=False,
            column_names=[association_id],
            required_in_prediction_requests=True,
    ),
    predictions_data_collection_settings=datarobot.DeploymentPredictionsDataCollectionSettingsArgs(
            enabled=True,
    ),
    health_settings=datarobot.DeploymentHealthSettingsArgs(
            data_drift=datarobot.DeploymentHealthSettingsDataDriftArgs(
                time_interval="P7D",
            ),
    ),
    predictions_by_forecast_date_settings=datarobot.DeploymentPredictionsByForecastDateSettingsArgs(
            enabled=True,
            column_name=date_col,
            datetime_format=datetime_format
    ),
    challenger_models_settings=datarobot.DeploymentChallengerModelsSettingsArgs(
            enabled=True,
    ),
    challenger_replay_settings=datarobot.DeploymentChallengerReplaySettingsArgs(
            enabled=True,
    ),
    segment_analysis_settings=datarobot.DeploymentSegmentAnalysisSettingsArgs(
            enabled=True,
            attributes=segment_analysis_attributes
    ),
)




retraining_policy_settings = DeploymentRetrainingPolicyArgs(
        resource_name=f"Retrain on Accuracy Decline {project_name}",
        description="",
        action=Action.ModelReplacement,
        autopilot_options=AutopilotOptions(
            mode=dr.enums.AUTOPILOT_MODE.QUICK,
            blend_best_models=False,
            shap_only_mode=False,
            run_leakage_removed_feature_list=True,
        ),
        trigger=Trigger(
            type=TriggerType.accuracy_decline,
                schedule=Schedule(
                    minutes=["0"],
                    hours=["0"],
                    day_of_months=["*"],
                    months=["*"],
                    day_of_weeks=["*"],
                ),
            status_declines_to_warning=True,
            status_declines_to_failing=False,
            status_still_in_decline=False,
        ),
        project_options_strategy=ProjectOptionsStrategy.SameAsChampion,
        feature_list_strategy=FeatureListStrategy.InformativeFeatures,
        model_selection_strategy=ModelSelectionStrategy.AutopilotRecommended,
        project_options=ProjectOptions(
            cv_method=CVMethod.RandomCV,
            validation_type=dr.enums.VALIDATION_TYPE.CV,
            reps=None,
            validation_pct=None,
            holdout_pct=None,
            metric=dr.enums.ACCURACY_METRIC.LOGLOSS,
        ),
)    
    

