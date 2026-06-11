from .reader import read_csv
from pyspark.sql import DataFrame
from config import DATA_PATH

def extract_dataset(spark) -> DataFrame:
    """
    Función de extracción de datos
    """
    df = read_csv(spark, DATA_PATH)
    return df