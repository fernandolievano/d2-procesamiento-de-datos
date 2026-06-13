from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from config import DATA_TRANSFORMED_PATH


AUDIO_FEATURES = [
    "danceability",
    "energy",
    "acousticness",
    "speechiness",
    "instrumentalness",
    "liveness",
    "valence",
]


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def format_number(value: int | float) -> str:
    return f"{value:,.0f}".replace(",", ".")


def apply_filters(
    df: pd.DataFrame,
    genres: list[str],
    popularity_tiers: list[str],
    explicit_options: list[str],
    popularity_range: tuple[int, int],
) -> pd.DataFrame:
    filtered_df = df.copy()

    if genres:
        filtered_df = filtered_df[filtered_df["track_genre"].isin(genres)]

    if popularity_tiers:
        filtered_df = filtered_df[filtered_df["popularity_tier"].isin(popularity_tiers)]

    explicit_map = {
        "Explicit": True,
        "Not explicit": False,
    }
    explicit_values = [explicit_map[item] for item in explicit_options]
    filtered_df = filtered_df[filtered_df["explicit"].isin(explicit_values)]

    min_popularity, max_popularity = popularity_range
    filtered_df = filtered_df[
        filtered_df["popularity"].between(min_popularity, max_popularity)
    ]

    return filtered_df


def show_metrics(df: pd.DataFrame) -> None:
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Tracks", format_number(len(df)))
    col2.metric("Generos", format_number(df["track_genre"].nunique()))
    col3.metric("Artistas", format_number(df["primary_artist"].nunique()))
    col4.metric("Popularidad prom.", f"{df['popularity'].mean():.1f}")
    col5.metric("Explicitas", f"{df['explicit'].mean() * 100:.1f}%")


def show_overview(df: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)

    genre_popularity = (
        df.groupby("track_genre", as_index=False)
        .agg(avg_popularity=("popularity", "mean"), tracks=("track_id", "count"))
        .sort_values("avg_popularity", ascending=False)
        .head(15)
    )
    genre_explicit = (
        df.groupby("track_genre", as_index=False)
        .agg(explicit_rate=("explicit", "mean"), tracks=("track_id", "count"))
        .assign(explicit_rate=lambda data: data["explicit_rate"] * 100)
        .sort_values("explicit_rate", ascending=False)
        .head(15)
    )

    with col1:
        fig = px.bar(
            genre_popularity,
            x="avg_popularity",
            y="track_genre",
            orientation="h",
            title="Generos con mayor popularidad promedio",
            labels={"avg_popularity": "Popularidad promedio", "track_genre": "Genero"},
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            genre_explicit,
            x="explicit_rate",
            y="track_genre",
            orientation="h",
            title="Generos con mayor proporcion de contenido explicito",
            labels={"explicit_rate": "% explicitas", "track_genre": "Genero"},
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "El dataset esta practicamente balanceado por genero, por eso se priorizan "
        "comparaciones de popularidad, contenido explicito y audio features."
    )


def show_popularity(df: pd.DataFrame) -> None:
    col1, col2 = st.columns(2)

    explicit_popularity = (
        df.groupby("explicit", as_index=False)
        .agg(avg_popularity=("popularity", "mean"), tracks=("track_id", "count"))
    )
    explicit_popularity["content"] = explicit_popularity["explicit"].map(
        {True: "Explicit", False: "Not explicit"}
    )

    with col1:
        fig = px.histogram(
            df,
            x="popularity",
            nbins=30,
            color="popularity_tier",
            title="Distribucion de popularidad",
            labels={"popularity": "Popularidad", "popularity_tier": "Nivel"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            explicit_popularity,
            x="content",
            y="avg_popularity",
            text="avg_popularity",
            title="Popularidad promedio por contenido explicito",
            labels={"content": "Contenido", "avg_popularity": "Popularidad promedio"},
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)


def show_audio_features(df: pd.DataFrame) -> None:
    feature_summary = (
        df.groupby("popularity_tier", as_index=False)[AUDIO_FEATURES]
        .mean()
        .melt(
            id_vars="popularity_tier",
            var_name="feature",
            value_name="value",
        )
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            feature_summary,
            x="feature",
            y="value",
            color="popularity_tier",
            barmode="group",
            title="Caracteristicas de audio por nivel de popularidad",
            labels={
                "feature": "Caracteristica",
                "value": "Valor promedio",
                "popularity_tier": "Popularidad",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        sample_df = df.sample(min(len(df), 5000), random_state=42)
        fig = px.scatter(
            sample_df,
            x="energy",
            y="danceability",
            color="popularity_tier",
            hover_data=["track_name", "primary_artist", "track_genre", "popularity"],
            title="Energia vs bailabilidad",
            labels={
                "energy": "Energy",
                "danceability": "Danceability",
                "popularity_tier": "Popularidad",
            },
        )
        st.plotly_chart(fig, use_container_width=True)


def show_tracks_table(df: pd.DataFrame) -> None:
    top_tracks = (
        df.sort_values("popularity", ascending=False)
        .loc[
            :,
            [
                "track_name",
                "primary_artist",
                "track_genre",
                "popularity",
                "duration_minutes",
                "explicit",
                "popularity_tier",
            ],
        ]
        .head(100)
    )

    st.dataframe(top_tracks, use_container_width=True, hide_index=True)


def show_findings(df: pd.DataFrame) -> None:
    genre_popularity = (
        df.groupby("track_genre")["popularity"]
        .mean()
        .sort_values(ascending=False)
    )
    explicit_popularity = df.groupby("explicit")["popularity"].mean()
    correlation = (
        df[AUDIO_FEATURES + ["popularity"]]
        .corr(numeric_only=True)["popularity"]
        .drop("popularity")
        .sort_values(key=lambda values: values.abs(), ascending=False)
    )

    top_genre = genre_popularity.index[0]
    top_genre_value = genre_popularity.iloc[0]
    explicit_diff = explicit_popularity.get(True, 0) - explicit_popularity.get(False, 0)
    top_feature = correlation.index[0]
    top_feature_value = correlation.iloc[0]

    st.subheader("Lectura rapida")
    st.write(
        f"- El genero con mayor popularidad promedio en el recorte actual es "
        f"**{top_genre}** ({top_genre_value:.1f})."
    )
    st.write(
        f"- La diferencia de popularidad promedio entre canciones explicitas y no "
        f"explicitas es de **{explicit_diff:.1f} puntos**."
    )
    st.write(
        f"- La caracteristica de audio con mayor asociacion lineal con popularidad "
        f"es **{top_feature}** (correlacion {top_feature_value:.2f})."
    )
    st.caption(
        "Estas lecturas son descriptivas: ayudan a explorar patrones, pero no prueban causalidad."
    )


def main() -> None:
    st.set_page_config(
        page_title="Spotify Tracks Dashboard",
        page_icon=":musical_note:",
        layout="wide",
    )

    st.title("Spotify Tracks Dashboard")
    st.caption(
        "Procesamiento de Datos - Desempeno 2 | Dashboard exploratorio basado "
        "en el dataset transformado por el ETL."
    )

    data_path = Path(DATA_TRANSFORMED_PATH)
    if not data_path.exists():
        st.error(f"No se encontro el archivo {DATA_TRANSFORMED_PATH}.")
        st.info("Ejecuta primero: python main.py")
        st.stop()

    df = load_data(DATA_TRANSFORMED_PATH)

    st.sidebar.header("Filtros")

    all_genres = sorted(df["track_genre"].dropna().unique())
    selected_genres = st.sidebar.multiselect(
        "Generos",
        options=all_genres,
        default=[],
        placeholder="Todos los generos",
    )

    all_tiers = sorted(df["popularity_tier"].dropna().unique())
    selected_tiers = st.sidebar.multiselect(
        "Nivel de popularidad",
        options=all_tiers,
        default=all_tiers,
    )

    selected_explicit = st.sidebar.multiselect(
        "Contenido explicito",
        options=["Explicit", "Not explicit"],
        default=["Explicit", "Not explicit"],
    )

    popularity_range = st.sidebar.slider(
        "Rango de popularidad",
        min_value=int(df["popularity"].min()),
        max_value=int(df["popularity"].max()),
        value=(int(df["popularity"].min()), int(df["popularity"].max())),
    )

    filtered_df = apply_filters(
        df,
        genres=selected_genres,
        popularity_tiers=selected_tiers,
        explicit_options=selected_explicit,
        popularity_range=popularity_range,
    )

    if filtered_df.empty:
        st.warning("No hay canciones para los filtros seleccionados.")
        st.stop()

    show_metrics(filtered_df)

    tab_overview, tab_popularity, tab_features, tab_findings, tab_tracks = st.tabs(
        ["Resumen", "Popularidad", "Audio features", "Hallazgos", "Top tracks"]
    )

    with tab_overview:
        show_overview(filtered_df)

    with tab_popularity:
        show_popularity(filtered_df)

    with tab_features:
        show_audio_features(filtered_df)

    with tab_findings:
        show_findings(filtered_df)

    with tab_tracks:
        show_tracks_table(filtered_df)


if __name__ == "__main__":
    main()
