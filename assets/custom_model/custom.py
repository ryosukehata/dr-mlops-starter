"""
Copyright 2021 DataRobot, Inc. and its affiliates.
All rights reserved.
This is proprietary source code of DataRobot, Inc. and its affiliates.
Released under the terms of DataRobot Tool and Utility Agreement.
"""
import pandas as pd

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    if 'ロット番号' in df.columns:
        df = df.drop(columns=["ロット番号"])
    df["塗布長"] = df["塗布長"].str[:-1].astype(int)
    df = df.drop(columns=["号機"])
    seizou_dict = {'製造': 0, '試作品': 1, '研究所テスト': 2, '製造部テスト': 3}
    df["種別"] = df["種別"].map(seizou_dict)
    return df

def transform(data, model):
    """
    Note: This hook may not have to be implemented for your model.
    In this case implemented for the model used in the example.
    Modify this method to add data transformation before scoring calls. For example, this can be
    used to implement one-hot encoding for models that don't include it on their own.
    Parameters
    ----------
    data: pd.DataFrame
    model: object, the deserialized model
    Returns
    -------
    pd.DataFrame
    """
    # Execute any steps you need to do before scoring
    # Remove target columns if they're in the dataset
    data = preprocess(data)
    data = data.fillna(data.mode().iloc[0])
    return data