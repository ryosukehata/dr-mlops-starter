import yaml
import pandas as pd
import datarobot as dr
from dotenv import load_dotenv

from infra.settings_main import model_training_output_path
from infra.settings_datasets import prediction_datasets, actual_dataset
from datarobotx.idp.datasets import get_or_create_dataset_from_df
from starter.schema import AppSettings
from typing import List


def preprocess_prediction_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
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


def add_prediction_and_retraining_data() -> List[str]:
    load_dotenv()
    client = dr.Client()

    with open(model_training_output_path) as f:
        model_training_output = AppSettings(**yaml.safe_load(f))
    use_case_id = model_training_output.use_case_id
    # Replace as needed with your own data ingest and/or preparation logic
    prediction_dataset_ids = []
    for prediction_dataset in prediction_datasets:
        df = preprocess_prediction_dataset(pd.read_csv(prediction_dataset.file_path))

        print("Uploading prediction data to AI Catalog...")
        prediction_dataset_id = get_or_create_dataset_from_df(
        endpoint=client.endpoint,
        token=client.token,
        data_frame=df,
        name=prediction_dataset.resource_name,
        use_cases=use_case_id,
        )
        prediction_dataset_ids.append(prediction_dataset_id)

    # 実データをアップロードする
    df = pd.read_csv(actual_dataset.file_path)
    print("Uploading actual data to AI Catalog...")

    actual_dataset_id =  get_or_create_dataset_from_df(
        endpoint=client.endpoint,
        token=client.token,
        data_frame=df,
        name=actual_dataset.resource_name,
        use_cases=use_case_id,
    )


    return prediction_dataset_ids, actual_dataset_id

def make_prediction(deployment_id, prediction_dataset_ids):

    for prediction_dataset_id in prediction_dataset_ids:
        # get to make sure it exists
    
        dataset = dr.Dataset.get(prediction_dataset_id)

        intake_settings={
            'type': 'dataset',
            'dataset': dataset
        }

        job = dr.BatchPredictionJob.score(
            deployment_id,
            intake_settings=intake_settings
        )
#    job.wait_for_completion()

def upload_actual(deployment_id:str, actual_dataset_id:str):
    load_dotenv()
    client = dr.Client()
    deploy = dr.Deployment.get(deployment_id)
    job = deploy.submit_actuals_from_catalog_async(actual_dataset_id, 
                                             actual_value_column="ブリードアウト", 
                                             association_id_column="ロット番号")

#    job.wait_for_completion()

def prediction_and_upload_actual(deployment_id:str):
    prediction_dataset_ids, actual_dataset_id = add_prediction_and_retraining_data()

    make_prediction(deployment_id=deployment_id, prediction_dataset_ids=prediction_dataset_ids)
    upload_actual(deployment_id=deployment_id, actual_dataset_id=actual_dataset_id)
