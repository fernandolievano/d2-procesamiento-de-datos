from pathlib import Path

from pyspark.sql import DataFrame

from config import DATA_TRANSFORMED_PATH
from utils.logger import get_logger

logger = get_logger(__name__)


def export_to_csv(df: DataFrame, output_path: str = DATA_TRANSFORMED_PATH) -> None:
    """
    Exporta el DataFrame transformado como un único archivo CSV.
    """
    target_path = Path(output_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Exportando DataFrame a CSV en {target_path}")
    df.toPandas().to_csv(target_path, index=False)
    logger.info("Exportacion completada exitosamente")
