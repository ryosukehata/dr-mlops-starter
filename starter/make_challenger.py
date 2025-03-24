import pandas as pd
from typing import List
import yaml


import datarobot as dr
from dotenv import load_dotenv

from infra.common.schema import (
    AdvancedOptionsArgs,
    AnalyzeAndModelArgs,
    AutopilotRunArgs,
)
from infra.settings_main import project_name, model_training_output_path
from datarobotx.idp.autopilot import get_or_create_autopilot_run
from datarobotx.idp.registered_model_versions import (
    get_or_create_registered_leaderboard_model_version,
)
from datarobotx.idp.datasets import get_or_create_dataset_from_df
from infra.settings_datasets import retraining_datasets

from starter.schema import AppSettings

from infra.settings_main import challenger_model_output_path



def preprocess_retraning_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    """Sample function showing how to execute arbitrary code on your dataset

    Parameters
    ----------
    dataset : pd.DataFrame
        A dataset we will preprocess

    Returns
    -------
    pd.DataFrame :
        Preprocessed dataset
    """
    return dataset


def training_and_registered_challenger_model() -> List[str]:
    load_dotenv()
    client = dr.Client()
    with open(model_training_output_path) as f:
        model_training_output = AppSettings(**yaml.safe_load(f))

    use_case_id=model_training_output.use_case_id
    retraining_dataset_ids = []
    for retraining_dataset in retraining_datasets:
        df = preprocess_retraning_dataset(pd.read_csv(retraining_dataset.file_path))

        print("Uploading retraning data to AI Catalog...")
        retraining_dataset_id = get_or_create_dataset_from_df(
            endpoint=client.endpoint,
            token=client.token,
            data_frame=df,
            name=retraining_dataset.resource_name,
            use_cases=use_case_id,
        )
        retraining_dataset_ids.append(retraining_dataset_id)

    
    registered_ids = []
    for retraning_dataset_id, retraining_dataset in zip(retraining_dataset_ids, retraining_datasets):
        print(retraning_dataset_id, retraining_dataset.resource_name)
    
        autopilotrun_args = AutopilotRunArgs(
            name=retraining_dataset.resource_name,
            advanced_options_config=AdvancedOptionsArgs(seed=42),
            analyze_and_model_config=AnalyzeAndModelArgs(
                metric="LogLoss",
                mode=dr.enums.AUTOPILOT_MODE.QUICK,
                target="ブリードアウト",
                worker_count=-1,
            ),
        )

        registered_model_name =  model_training_output.registered_model_name
        print("Running Autopilot...")
        project_id = get_or_create_autopilot_run(
            endpoint=client.endpoint,
            token=client.token,
            dataset_id=retraning_dataset_id,
            use_case=use_case_id,
            **autopilotrun_args.model_dump(),
        )



        model_id = dr.ModelRecommendation.get(project_id).model_id

        print("Registered recommended model...")
        registered_model_version_id = get_or_create_registered_leaderboard_model_version(
            endpoint=client.endpoint,
            token=client.token,
            model_id=model_id,
            registered_model_name=registered_model_name,
            prediction_threshold=0.5,
        )
        registered_ids.append(registered_model_version_id)
    return registered_ids


def create_challangers(registered_ids: List[str], deployment_id:str, prediction_environment_id:str):
    load_dotenv()

    client = dr.Client()
    registered_id_dict = {}
    for num, registered_id in enumerate(registered_ids):
        name = "retraining_dataset_"+str(num+1)
        challenger = dr.models.deployment.challenger.Challenger.create(
            deployment_id=deployment_id,
            model_package_id=registered_id,
            name=name,
            prediction_environment_id=prediction_environment_id
        )
        registered_id_dict[name] = registered_id
    return registered_id_dict

def train_and_create_challangers(deployment_id:str, prediction_environment_id:str):
    registered_ids=training_and_registered_challenger_model()
    registered_id_dict = create_challangers(registered_ids=registered_ids, deployment_id=deployment_id, prediction_environment_id=prediction_environment_id)

    with open(challenger_model_output_path, 'w') as f:
        yaml.dump(registered_id_dict, f)