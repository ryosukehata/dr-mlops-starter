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

from __future__ import annotations

from typing import Any, List, Optional, Tuple

import datarobot as dr
import pulumi_datarobot as datarobot
from pydantic import BaseModel, ConfigDict

from infra.common.schema_retraining import (
    AutopilotOptions,
    ProjectOptions,
    TimeSeriesOptions,
    Trigger,
)

from .globals import (
    GlobalPredictionEnvironmentPlatforms,
)


class DeploymentArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_name: str
    label: str
    association_id_settings: datarobot.DeploymentAssociationIdSettingsArgs | None = None
    bias_and_fairness_settings: (
        datarobot.DeploymentBiasAndFairnessSettingsArgs | None
    ) = None
    challenger_models_settings: (
        datarobot.DeploymentChallengerModelsSettingsArgs | None
    ) = None
    challenger_replay_settings: (
        datarobot.DeploymentChallengerReplaySettingsArgs | None
    ) = None
    drift_tracking_settings: datarobot.DeploymentDriftTrackingSettingsArgs | None = None
    health_settings: datarobot.DeploymentHealthSettingsArgs | None = None
    importance: str | None = None
    prediction_intervals_settings: (
        datarobot.DeploymentPredictionIntervalsSettingsArgs | None
    ) = None
    prediction_warning_settings: (
        datarobot.DeploymentPredictionWarningSettingsArgs | None
    ) = None
    predictions_by_forecast_date_settings: (
        datarobot.DeploymentPredictionsByForecastDateSettingsArgs | None
    ) = None
    predictions_data_collection_settings: (
        datarobot.DeploymentPredictionsDataCollectionSettingsArgs | None
    ) = None
    predictions_settings: datarobot.DeploymentPredictionsSettingsArgs | None = None
    segment_analysis_settings: (
        datarobot.DeploymentSegmentAnalysisSettingsArgs | None
    ) = None


class DatasetArgs(BaseModel):
    resource_name: str
    file_path: str
    name: str | None = None


class UseCaseArgs(BaseModel):
    resource_name: str
    name: str | None = None
    description: str | None


class PredictionEnvironmentArgs(BaseModel):
    resource_name: str
    name: str | None = None
    platform: GlobalPredictionEnvironmentPlatforms


class AdvancedOptionsArgs(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    weights: str | None = None
    response_cap: bool | float | None = None
    blueprint_threshold: int | None = None
    seed: int | None = None
    smart_downsampled: bool | None = None
    majority_downsampling_rate: float | None = None
    offset: List[str] | None = None
    exposure: str | None = None
    accuracy_optimized_mb: bool | None = None
    scaleout_modeling_mode: str | None = None
    events_count: str | None = None
    monotonic_increasing_featurelist_id: str | None = None
    monotonic_decreasing_featurelist_id: str | None = None
    only_include_monotonic_blueprints: bool | None = None
    allowed_pairwise_interaction_groups: List[Tuple[str, ...]] | None = None
    blend_best_models: bool | None = None
    scoring_code_only: bool | None = None
    prepare_model_for_deployment: bool | None = None
    consider_blenders_in_recommendation: bool | None = None
    min_secondary_validation_model_count: int | None = None
    shap_only_mode: bool | None = None
    autopilot_data_sampling_method: str | None = None
    run_leakage_removed_feature_list: bool | None = None
    autopilot_with_feature_discovery: bool | None = False
    feature_discovery_supervised_feature_reduction: bool | None = None
    exponentially_weighted_moving_alpha: float | None = None
    external_time_series_baseline_dataset_id: str | None = None
    use_supervised_feature_reduction: bool | None = True
    primary_location_column: str | None = None
    protected_features: List[str] | None = None
    preferable_target_value: str | None = None
    fairness_metrics_set: str | None = None
    fairness_threshold: str | None = None
    bias_mitigation_feature_name: str | None = None
    bias_mitigation_technique: str | None = None
    include_bias_mitigation_feature_as_predictor_variable: bool | None = None
    default_monotonic_increasing_featurelist_id: str | None = None
    default_monotonic_decreasing_featurelist_id: str | None = None
    model_group_id: str | None = None
    model_regime_id: str | None = None
    model_baselines: List[str] | None = None
    incremental_learning_only_mode: bool | None = None
    incremental_learning_on_best_model: bool | None = None
    chunk_definition_id: str | None = None
    incremental_learning_early_stopping_rounds: int | None = None


class AnalyzeAndModelArgs(BaseModel):
    target: Any | None = None
    mode: Any = dr.enums.AUTOPILOT_MODE.QUICK
    metric: Any | None = None
    worker_count: Any | None = None
    positive_class: Any | None = None
    partitioning_method: Any | None = None
    featurelist_id: Any | None = None
    advanced_options: Any | None = None
    max_wait: int = dr.enums.DEFAULT_MAX_WAIT
    target_type: Any | None = None
    credentials: Any | None = None
    feature_engineering_prediction_point: Any | None = None
    unsupervised_mode: bool = False
    relationships_configuration_id: Any | None = None
    class_mapping_aggregation_settings: Any | None = None
    segmentation_task_id: Any | None = None
    unsupervised_type: Any | None = None
    autopilot_cluster_list: Any | None = None
    use_gpu: Any | None = None


class AutopilotRunArgs(BaseModel):
    name: str
    analyze_and_model_config: AnalyzeAndModelArgs | None = None
    advanced_options_config: AdvancedOptionsArgs | None = None


class ApplicationSourceArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    resource_name: str
    base_environment_id: str
    files: Optional[Any] = None
    folder_path: Optional[str] = None
    name: Optional[str] = None


class DeploymentRetrainingPolicyArgs(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    resource_name: str
    action: str | None = None
    autopilot_options: AutopilotOptions | None = None
    description: str | None = None
    feature_list_strategy: str | None = None
    model_selection_strategy: str | None = None
    name: str | None = None
    project_options: ProjectOptions | None = None
    project_options_strategy: str | None = None
    time_series_options: TimeSeriesOptions | None = None
    trigger: Trigger | None = None