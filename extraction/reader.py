from utils.logger import get_logger

logger = get_logger(__name__)

def read_csv(spark, path):
    """
    Lee un archivo CSV y devuelve un DataFrame de Spark.
    """
    logger.info("Leyendo dataset...")
    df = spark.read.option("header", True).option("inferSchema", True).option("escape", '"').csv(path)
    logger.info(f"Dataset cargado correctamente")

    return df