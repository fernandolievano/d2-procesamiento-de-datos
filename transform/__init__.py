from .cleaning import clean_dataset
from .features import create_features
from pyspark.sql import DataFrame

def transform_dataset(df: DataFrame) -> DataFrame:
    df = clean_dataset(df)
    df = create_features(df)

    return df

__all__ = ['transform_dataset']