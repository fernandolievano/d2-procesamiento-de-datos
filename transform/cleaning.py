from utils.logger import get_logger
from pyspark.sql import DataFrame

logger = get_logger(__name__)

COLUMNS_TO_DROP = ["_c0", "Unnamed: 0"]

def clean_dataset(df: DataFrame) -> DataFrame:
    """
    Realiza la limpieza de datos en el DataFrame,
    eliminando filas con valores nulos y duplicados
    """
    logger.info("Iniciando limpieza del DataFrame")
    df = drop_unnecessary_columns(df, COLUMNS_TO_DROP)
    df = drop_rows_with_nulls(df)
    df = drop_duplicate_rows(df)
    logger.info("Limpieza del DataFrame finalizada")

    return df

def drop_unnecessary_columns(df: DataFrame, columns_to_drop: list) -> DataFrame:
    """
    Elimina columnas innecesarias del DataFrame
    """
    logger.info(f"Eliminando columnas innecesarias: {columns_to_drop}")
    df = df.drop(*columns_to_drop)

    return df

def drop_rows_with_nulls(df: DataFrame) -> DataFrame:
    """
    Elimina filas que contienen valores nulos
    """
    logger.info("Eliminando filas con valores nulos")
    df = df.na.drop()

    return df

def drop_duplicate_rows(df: DataFrame) -> DataFrame:
    """
    Elimina filas duplicadas del DataFrame
    """
    logger.info("Eliminando filas duplicadas")
    df = df.dropDuplicates()

    return df