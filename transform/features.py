from utils.logger import get_logger
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

logger = get_logger(__name__)

def create_features(df: DataFrame) -> DataFrame:
    """
    Crea nuevas características a partir de las existentes en el DataFrame
    """
    df = add_duration_minutes(df)

    return df

def add_duration_minutes(df: DataFrame) -> DataFrame:
    """
    Agrega una columna 'duration_minutes' calculada a partir de 'duration_ms'.
    """
    logger.info('Agregando columna duration_minutes calculada a partir de duration_ms')
    df = df.withColumn('duration_minutes', col('duration_ms') / 60000)

    return df