def read_csv(spark, path):
    """
    Lee un archivo CSV y devuelve un DataFrame de Spark.
    """
    return spark.read.csv(path)