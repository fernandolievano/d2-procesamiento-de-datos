from utils.logger import get_logger
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, split, when

logger = get_logger(__name__)

# CONSTANTES
MS_IN_A_MINUTE = 60000
# umbrales de popularidad
LOW_POPULARITY_LIMIT = 30
MEDIUM_POPULARITY_LIMIT = 70
HIGH_POPULARITY_LIMIT = 90
# umbrales de tempo (BPM)
SLOW_TEMPO_LIMIT = 90
MEDIUM_TEMPO_LIMIT = 120
FAST_TEMPO_LIMIT = 140
# umbral de valence (positividad)
VALENCE_MOOD_THRESHOLD = 0.5

def create_features(df: DataFrame) -> DataFrame:
    """
    Crea nuevas caracteristicas a partir de las existentes en el DataFrame
    """
    logger.info("Iniciando creacion de nuevas caracteristicas (feature engineering)")

    df = add_duration_minutes(df)
    df = add_primary_artist(df)
    df = add_popularity_tier(df)
    df = add_tempo_class(df)
    df = add_valence_mood(df)
    return df

def add_duration_minutes(df: DataFrame) -> DataFrame:
    """
    Agrega una columna 'duration_minutes' calculada a partir de 'duration_ms'.
    """
    logger.info("Agregando columna 'duration_minutes'")
    return df.withColumn('duration_minutes', col('duration_ms') / MS_IN_A_MINUTE)

def add_primary_artist(df: DataFrame) -> DataFrame:
    """
    Extrae el primer artista listado de la columna 'artists'.
    """
    logger.info("Agregando columna 'primary_artist'")

    # se asume que los artistas están separados por ';' en la columna 'artists'
    return df.withColumn("primary_artist", split(col("artists"), ";")[0])

def add_popularity_tier(df: DataFrame) -> DataFrame:
    """
    Segmenta la popularidad en categorías (LOW, MEDIUM, HIGH) basadas en umbrales predefinidos.
    """
    logger.info("Agregando columna 'popularity_tier'")

    return df.withColumn(
        'popularity_tier',
         when(col("popularity") <= LOW_POPULARITY_LIMIT, "Low")
        .when(col("popularity") <= MEDIUM_POPULARITY_LIMIT, "Medium")
        .when(col("popularity") <= HIGH_POPULARITY_LIMIT, "High")
        .otherwise("Top/Viral")
    )

def add_tempo_class(df: DataFrame) -> DataFrame:
    """
    Clasifica el tempo en categorías según el BPM (Slow, Medium, Fast)
    """
    logger.info("Agregando columna 'tempo_class'")

    return df.withColumn(
        'tempo_class',
         when(col("tempo") < SLOW_TEMPO_LIMIT, "Slow")
        .when(col("tempo") < MEDIUM_TEMPO_LIMIT, "Medium")
        .when(col("tempo") < FAST_TEMPO_LIMIT, "Fast")
        .otherwise("Upbeat")
    )

def add_valence_mood(df: DataFrame) -> DataFrame:
    """Determina si la canción tiene una vibra alegre/enérgica o melancólica/oscura."""
    logger.info("Agregando columna 'valence_mood'")

    return df.withColumn(
        "valence_mood",
        when(col("valence") < VALENCE_MOOD_THRESHOLD, "Melancholic/Dark")
        .otherwise("Happy/Energetic")
    )