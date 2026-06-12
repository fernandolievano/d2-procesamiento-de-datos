import os
from utils.logger import get_logger
from pyspark.sql import DataFrame
from config import OUTPUT_PATH

logger = get_logger(__name__)

def export_to_csv(df: DataFrame, filename: str) -> None:
    """
    Exporta un DataFrame de Spark a Pandas y lo exporta como un único archivo CSV.
    """
    # asegurarse de que la carpeta outputs exista
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    target_path = os.path.join(OUTPUT_PATH, filename)
    logger.info(f"Exportando DataFrame a Pandas y guardando en {target_path}")

    # conversión y exportación
    pandas_df = df.toPandas()
    pandas_df.to_csv(target_path, index=False)

    logger.info("Exportacion completada exitosamente")