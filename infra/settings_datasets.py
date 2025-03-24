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


from .common.schema import DatasetArgs
from .settings_main import project_name

training_dataset = DatasetArgs(
    resource_name=f"Predictive AI MLOps Starter Training Data [{project_name}]",
    file_path="assets/コーティング製品ブリードアウトmain_train.csv",
)

prediction_datasets = [DatasetArgs(
    resource_name=f"Prediction data for data drift Accuracy: [{project_name}]",
    file_path="../assets/prediction_data.csv",
)]

actual_dataset =  DatasetArgs(
    resource_name=f"Predictive AI MLOps Starter Actual [{project_name}]",
    file_path="../assets/prediction_data_actual.csv",
)

retraining_datasets = [DatasetArgs(
    resource_name=f"Predictive AI MLOps Starter Retraining Data 01 [{project_name}]",
    file_path="../assets/再学習用データ01.csv",
),
                     DatasetArgs(
    resource_name=f"Predictive AI MLOps Starter Retraining Data 02 [{project_name}]",
    file_path="../assets/再学習用データ02.csv",
),
#                     DatasetArgs(
#    resource_name=f"Predictive AI MLOps Starter Retraining Data 03 [{project_name}]",
#    file_path="../assets/再学習用データ03.csv",
#)
                      ]
