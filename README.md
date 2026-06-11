# Desempeño 2 - Procesamiento de Datos

### EDA a gran escala con PySpark

**Tecnologías usadas:**

- PySpark
- Streamlit
- Plotly

**Conceptos vistos en clase aplicados**:

- ETL
- EDA
- Paralelización
- Visualización

---

## Dataset

### Descripción

Este proyecto utiliza un dataset de canciones obtenido desde Spotify. Cada registro representa una canción e incluye información descriptiva (artista, álbum, género) junto con métricas de audio utilizadas para análisis musical y sistemas de recomendación.

### Estructura del Dataset

| Columna | Tipo | Descripción |
|----------|------|-------------|
| track_id | String | Identificador único de la canción |
| artists | String | Artista(s) de la canción |
| album_name | String | Nombre del álbum |
| track_name | String | Nombre de la canción |
| popularity | String | Popularidad de la canción en Spotify |
| duration_ms | String | Duración en milisegundos |
| explicit | String | Indica si contiene contenido explícito |
| danceability | String | Medida de qué tan adecuada es la canción para bailar |
| energy | String | Nivel de energía e intensidad percibida |
| key | String | Tonalidad musical |
| loudness | String | Volumen promedio en decibelios |
| mode | String | Modalidad musical (mayor o menor) |
| speechiness | String | Presencia de palabras habladas |
| acousticness | String | Probabilidad de que la canción sea acústica |
| instrumentalness | Double | Probabilidad de que la canción sea instrumental |
| liveness | String | Presencia de audiencia o interpretación en vivo |
| valence | String | Positividad musical percibida |
| tempo | Double | Tempo estimado en BPM |
| time_signature | Double | Compás musical |
| track_genre | String | Género principal de la canción |