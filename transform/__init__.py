from .cleaning import clean_dataset
from pyspark.sql import DataFrame

def transform_dataset(df: DataFrame) -> DataFrame:
    df = clean_dataset(df)

    return df

__all__ = ['transform_dataset']