import shutil
from pathlib import Path

from pyspark.sql import DataFrame

from config import DATA_TRANSFORMED_PATH
from utils.logger import get_logger

logger = get_logger(__name__)


def export_to_csv(df: DataFrame, output_path: str = DATA_TRANSFORMED_PATH) -> None:
    """
    Exporta un DataFrame de Spark como un unico archivo CSV.
    """
    target_path = Path(output_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = target_path.parent / f".{target_path.stem}_spark_output"
    if temp_path.exists():
        shutil.rmtree(temp_path)
    if target_path.exists():
        target_path.unlink()

    logger.info(f"Exportando DataFrame con Spark en {target_path}")
    df.coalesce(1).write.mode("overwrite").option("header", True).csv(str(temp_path))

    part_file = next(temp_path.glob("part-*.csv"), None)
    if part_file is None:
        raise FileNotFoundError(f"No se encontro el archivo CSV generado en {temp_path}")

    shutil.move(str(part_file), target_path)
    shutil.rmtree(temp_path)

    logger.info("Exportacion completada exitosamente")
