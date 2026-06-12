# Desempeño 2 - Procesamiento de Datos

### EDA a gran escala con PySpark

## Tecnologías usadas
- PySpark
- Plotly
- Streamlit (pendiente)

## Conceptos vistos en clase aplicados
- ETL
- EDA
- Paralelización
- Visualización

## Estado actual
- Pipeline ETL implementado.
- Notebook de EDA en desarrollo.
- Dashboard con Streamlit pendiente.

## Ejecución

```
python main.py
```

El pipeline genera `outputs/transformed_dataset.csv`.

## Preguntas del EDA
- ¿Qué géneros son más populares?
- ¿Qué artistas predominan en la lista?
- ¿Cómo se distribuye la duración de las canciones según su género?
- ¿Qué factores influyen en la popularidad de las canciones?
- ¿El contenido explícito afecta la popularidad de los tracks?
- ¿Qué características de audio (danceability, acousticness, energy) tienen las canciones más populares?

## Dataset

### Estructura del Dataset

| Columna | Tipo | Descripción |
|----------|------|-------------|
| track_id | String | Identificador único de la canción |
| artists | String | Artista(s) de la canción |
| album_name | String | Nombre del álbum |
| track_name | String | Nombre de la canción |
| popularity | Integer | Popularidad de la canción en Spotify |
| duration_ms | Integer | Duración en milisegundos |
| explicit | Boolean | Indica si contiene contenido explícito |
| danceability | Double | Medida de qué tan adecuada es la canción para bailar |
| energy | Double | Nivel de energía e intensidad percibida |
| key | Integer | Tonalidad musical |
| loudness | Double | Volumen promedio en decibelios |
| mode | Integer | Modalidad musical |
| speechiness | Double | Presencia de palabras habladas |
| acousticness | Double | Probabilidad de que la canción sea acústica |
| instrumentalness | Double | Probabilidad de que la canción sea instrumental |
| liveness | Double | Presencia de audiencia o interpretación en vivo |
| valence | Double | Positividad musical percibida |
| tempo | Double | Tempo estimado en BPM |
| time_signature | Integer | Compás musical |
| track_genre | String | Género principal de la canción |
