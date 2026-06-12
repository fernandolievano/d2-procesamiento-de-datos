from config import SPARK_APP_NAME
from utils.logger import get_logger
from spark.session import create_spark_session
from extraction import extract_dataset
from analysis import profiling
from transform import transform_dataset
from load import load_dataset

logger = get_logger(__name__)

# Programa Principal
def main():
    logger.info('Iniciando programa principal')
    spark = create_spark_session(app_name=SPARK_APP_NAME)

    try:
        # -> Extraction
        raw_df = extract_dataset(spark)
        profiling(df=raw_df, stage='extraction')

        # -> Transformation
        transformed_df = transform_dataset(raw_df)
        profiling(df=transformed_df, stage='transformation')

        # -> Load
        load_dataset(transformed_df)

    except Exception as e:
        logger.exception('Error al ejecutar el programa principal')
        raise
    finally:
        spark.stop()
        logger.info('Programa principal finalizado')


if __name__ == '__main__':
    main()
