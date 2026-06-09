from utils.logger import get_logger
from pyspark.sql import DataFrame

logger = get_logger(__name__)

def profiling(df: DataFrame):
    """
    Realizar un perfilado básico del DataFrame.
    """
    logger.info("Iniciando perfilado del DataFrame")

    show_schema(df)
    analyze_data_types(df)
    count_rows(df)
    count_columns(df)
    count_nulls_by_column(df)
    count_rows_with_nulls(df)
    find_duplicates(df)

def show_schema(df: DataFrame):
    """
    Mostrar el esquema del DataFrame.
    """
    logger.info("Esquema del DataFrame:")
    df.printSchema()

def analyze_data_types(df: DataFrame):
    logger.info("Tipos de datos detectados:")

    for field in df.schema.fields:
        logger.info(f"{field.name}: {field.dataType}")

def count_rows(df: DataFrame):
    """
    Contar el número de filas en el DataFrame.
    """
    count = df.count()
    logger.info(f"Numero de filas: {count}")

    return count

def count_columns(df: DataFrame):
    """
    Contar el número de columnas en el DataFrame.
    """
    count = len(df.columns)
    logger.info(f"Numero de columnas: {count}")

    return count

def count_nulls_by_column(df: DataFrame):
    """
    Encontrar el número de valores nulos en cada columna del DataFrame.
    """
    null_counts = {}

    for column in df.columns:
        null_count = df.filter(df[column].isNull()).count()
        null_counts[column] = null_count
        logger.info(f"Columna '{column}': {null_count} valores nulos")

    return null_counts

def count_rows_with_nulls(df: DataFrame):
    """
    Encontrar cantidad de filas con valores nulos en las columnas detectadas
    (artists, album_name, track_name).
    """
    rows_with_nulls = df.filter(df.artists.isNull() | df.album_name.isNull() | df.track_name.isNull()).count()
    logger.info(f"Cantidad de filas con valores nulos: {rows_with_nulls}")
    return rows_with_nulls

def find_duplicates(df: DataFrame):
    total = df.count()
    unique = df.dropDuplicates().count()
    duplicates = total - unique
    logger.info(f"Duplicados: {duplicates} (Total: {total}, Unicos: {unique})")

    return duplicates