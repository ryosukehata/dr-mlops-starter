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
from urllib.parse import urljoin

import datarobot as dr
import yaml
from pydantic import ValidationError

sys.path.append("..")

from starter.i18n import gettext
from starter.resources import Deployment, ScoringDataset, app_settings_file_name
from starter.schema import (
    AppSettings,
    AppUrls,
)

try:
    with open(app_settings_file_name) as f:
        app_settings = AppSettings(**yaml.safe_load(f))

    deployment_id = Deployment().id
    scoring_dataset_id = ScoringDataset().id
except (FileNotFoundError, ValidationError) as e:
    raise ValueError(
        gettext(
            "Unable to load Deployment IDs or Application Settings. "
            "If running locally, verify you have selected the correct "
            "stack and that it is active using `pulumi stack output`. "
            "If running in DataRobot, verify your runtime parameters have been set correctly."
        )
    ) from e


def get_app_settings() -> AppSettings:
    return app_settings


def get_app_urls() -> AppUrls:
    base_url = urljoin(dr.Client().endpoint, "..")  # type: ignore[attr-defined]
    use_case_url = base_url + f"usecases/{app_settings.use_case_id}/overview"
    project_url = (
        base_url + f"projects/{app_settings.project_id}/models/{app_settings.model_id}/"
    )
    deployment_url = base_url + f"deployments/{deployment_id}/overview"
    return AppUrls(
        use_case=use_case_url,
        project=project_url,
        deployment=deployment_url,
    )
