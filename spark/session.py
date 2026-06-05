from pyspark.sql import SparkSession

def create_spark_session(app_name: str) -> SparkSession:
    """
    Crea una sesión de Spark.
    """
    return (
        SparkSession.builder.appName(app_name).getOrCreate()
    )