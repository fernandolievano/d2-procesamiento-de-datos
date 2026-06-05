from config import SPARK_APP_NAME, DATA_PATH
from utils.logger import get_logger
from spark.session import create_spark_session
from extraction.reader import read_csv

logger = get_logger(__name__)

# Programa Principal
def main():
  logger.info('Iniciando programa principal')

  spark = create_spark_session(app_name=SPARK_APP_NAME)

  try:
    # Extraction
    df_raw = read_csv(spark, DATA_PATH)
  except Exception as e:
    logger.error('Error al ejecutar el programa principal')
    raise
  finally:
    spark.stop()
    logger.info('Programa principal finalizado')


if __name__ == '__main__':
  main()