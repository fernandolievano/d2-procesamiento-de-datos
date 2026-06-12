import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

NUMERIC_COLUMNS = [
    "popularity",
    "duration_ms",
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]

AUDIO_FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "acousticness",
    "speechiness",
    "instrumentalness",
    "liveness",
    "valence",
]

CORRELATION_COLUMNS = [
    "popularity",
    "danceability",
    "energy",
    "acousticness",
    "speechiness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]


def describe_numeric_columns(df: DataFrame) -> DataFrame:
    return df.select(*NUMERIC_COLUMNS).describe()


def audio_features_to_pandas(df: DataFrame) -> pd.DataFrame:
    return (
        df.select(*AUDIO_FEATURE_COLUMNS)
        .toPandas()
        .melt(var_name="feature", value_name="value")
    )


def calculate_correlation_matrix(df: DataFrame) -> pd.DataFrame:
    correlation_matrix = pd.DataFrame(
        index=CORRELATION_COLUMNS,
        columns=CORRELATION_COLUMNS,
    )

    for col1 in CORRELATION_COLUMNS:
        for col2 in CORRELATION_COLUMNS:
            correlation_matrix.loc[col1, col2] = df.stat.corr(col1, col2)

    return correlation_matrix.astype(float)


def calculate_correlation(df: DataFrame, column: str) -> float:
    return df.stat.corr("popularity", column)


def calculate_genre_popularity(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("track_genre")
        .agg(F.avg("popularity").alias("avg_popularity"))
        .orderBy(F.desc("avg_popularity"))
    )


def genre_duration_to_pandas(df: DataFrame, limit: int = 10) -> pd.DataFrame:
    top_genres = [
        row["track_genre"]
        for row in calculate_genre_popularity(df).limit(limit).collect()
    ]

    return (
        df.filter(F.col("track_genre").isin(top_genres))
        .select("track_genre", "duration_minutes")
        .toPandas()
    )


def genre_audio_features_to_pandas(df: DataFrame, limit: int = 15) -> pd.DataFrame:
    genre_features = (
        df.groupBy("track_genre")
        .agg(
            F.avg("popularity").alias("avg_popularity"),
            F.avg("danceability").alias("danceability"),
            F.avg("energy").alias("energy"),
            F.avg("acousticness").alias("acousticness"),
            F.avg("speechiness").alias("speechiness"),
            F.avg("instrumentalness").alias("instrumentalness"),
            F.avg("liveness").alias("liveness"),
            F.avg("valence").alias("valence"),
        )
        .orderBy(F.desc("avg_popularity"))
        .limit(limit)
        .drop("avg_popularity")
    )

    return genre_features.toPandas().melt(
        id_vars="track_genre",
        var_name="feature",
        value_name="value",
    )


def calculate_artist_presence(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("primary_artist")
        .count()
        .orderBy(F.desc("count"))
    )


def calculate_artist_popularity(df: DataFrame) -> DataFrame:
    return (
        df.groupBy("primary_artist")
        .agg(
            F.count("*").alias("track_count"),
            F.avg("popularity").alias("avg_popularity"),
        )
        .filter(F.col("track_count") >= 3)
        .orderBy(F.desc("avg_popularity"))
    )


def popularity_tier_features_to_pandas(df: DataFrame) -> pd.DataFrame:
    tier_features = (
        df.groupBy("popularity_tier")
        .agg(
            F.avg("danceability").alias("danceability"),
            F.avg("energy").alias("energy"),
            F.avg("acousticness").alias("acousticness"),
            F.avg("speechiness").alias("speechiness"),
            F.avg("instrumentalness").alias("instrumentalness"),
            F.avg("liveness").alias("liveness"),
            F.avg("valence").alias("valence"),
            F.avg("tempo").alias("tempo"),
        )
    )

    return tier_features.toPandas().melt(
        id_vars="popularity_tier",
        var_name="feature",
        value_name="value",
    )


def top_tracks_audio_features_to_pandas(df: DataFrame, limit: int = 100) -> pd.DataFrame:
    return (
        df.orderBy(F.desc("popularity"))
        .limit(limit)
        .select(*AUDIO_FEATURE_COLUMNS)
        .toPandas()
        .melt(var_name="feature", value_name="value")
    )


def popularity_factors_to_pandas(df: DataFrame) -> pd.DataFrame:
    rows = []

    for column in CORRELATION_COLUMNS:
        if column != "popularity":
            correlation = calculate_correlation(df, column)
            rows.append(
                {
                    "feature": column,
                    "correlation": correlation,
                    "abs_correlation": abs(correlation),
                }
            )

    return (
        pd.DataFrame(rows)
        .sort_values("abs_correlation", ascending=False)
    )


def explicit_distribution_to_pandas(df: DataFrame) -> pd.DataFrame:
    return (
        df.groupBy("explicit")
        .count()
        .orderBy("explicit")
        .toPandas()
    )


def explicit_popularity_to_pandas(df: DataFrame) -> pd.DataFrame:
    return (
        df.groupBy("explicit")
        .agg(
            F.count("*").alias("track_count"),
            F.avg("popularity").alias("avg_popularity"),
        )
        .orderBy("explicit")
        .toPandas()
    )


def explicit_audio_features_to_pandas(df: DataFrame) -> pd.DataFrame:
    explicit_features = (
        df.groupBy("explicit")
        .agg(
            F.avg("danceability").alias("danceability"),
            F.avg("energy").alias("energy"),
            F.avg("acousticness").alias("acousticness"),
            F.avg("speechiness").alias("speechiness"),
            F.avg("instrumentalness").alias("instrumentalness"),
            F.avg("liveness").alias("liveness"),
            F.avg("valence").alias("valence"),
        )
    )

    return explicit_features.toPandas().melt(
        id_vars="explicit",
        var_name="feature",
        value_name="value",
    )
