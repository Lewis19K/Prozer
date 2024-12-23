# Prueba técnica Prozer

Para realizar la prueba se programó una API con FastAPI que realiza scraping de datos desde una URL proporcionada, procesa el contenido utilizando un modelo de inteligencia artificial y devuelve el resultado en formato JSON. El proyecto también guarda las respuestas en una base de datos SQLite.

## Funcionalidades

El proyecto inclute tres endpoints que fueron solicitadosÑ

1. `/scrape`: Recibe una URL de un sitio de noticias como [elmostrador.cl](https://elmostrador.cl/) y extrae los títulos y descripciones de los artículos de ese sitio. Además, el resultado de la extracción se almacena en una tabla de la base de datos, llamada `scraped_data`.

    Entrada:

    ```json
    {
    "url": "https://example.com"
    }
    ```

    Salida:

    ```json
    {
    "url": "https://example.com",
    "content": {
        "titles": ["Título 1", "Título 2"],
        "descriptions": ["Descripción 1", "Descripción 2"]
    }
    }
    ```

2. `/process`: Recibe un texto y devuelve un resultado de sentimiento de la clasificación de sentimientos de la API de transformers llamada `sentiment-analysis`.

    Entrada:

    ```json
    {
    "text": "Me siento muy feliz hoy"
    }
    ```

    Salida:

    ```json
    {
    "text": "Me siento muy feliz hoy",
    "result": [
        {
        "label": "POSITIVE",
        "score": 0.9998
        }
    ]
    }
    ```

3. `/combined`: Recibe una URL de una noticia como las del sitio [elmostrador.cl](https://elmostrador.cl/), realiza scraping de datos y procesa el contenido utilizando un modelo de inteligencia artificial y devuelve el resultado en formato JSON. Además, almacena los resultados en una tabla de la base de datos, llamada `combined_results`.

    Entrada:

    ```json
    {
    "url": "https://elmostrador.cl/noticias/pais/2024/12/21/chile-buscara-incorporar-el-paisaje-cultural-del-pisco-a-la-lista-de-patrimonio-mundial-de-la-unesco/"
    }
    ```

    Salida:

    ```json
    {
    "url": "https://elmostrador.cl/noticias/pais/2024/12/21/chile-buscara-incorporar-el-paisaje-cultural-del-pisco-a-la-lista-de-patrimonio-mundial-de-la-unesco/",
    "scraped_content": {
        "titles": [
        "Chile buscará incorporar el paisaje cultural del pisco a la lista de patrimonio mundial de la UNESCO"
        ],
        "descriptions": [
        "El Consejo de Ministros de Chile ha aprobado el plan de acción de la Organización Mundial del Patrimonio Cultural (UNESCO) para el año 2025, que incluye la incorporación del paisaje cultural del pisco en la lista de patrimonio mundial. El plan de acción se ha presentado en el Congreso de la Unión Europea y se está en proceso de aprobación por el Consejo de Ministros de Chile."
        ]
    },
    "processed_result": [
        {
        "label": "POSITIVE",
        "score": 0.9998
        }
    ]
    }
    ```

## Base de datos

El proyecto utiliza una base de datos SQLite para almacenar los resultados de los endpoints en tres tablas: `scraped_data`, `processed_data` y `combined_results`.

Cada tabla tiene una estructura básica con un ID autoincremental y campos para almacenar los datos.

## Requerimientos

Este proyecto se realizó utilizando Python 3.10 y FastAPI. A continuación se presentan las dependencias requeridas para ejecutar el proyecto:

- FastAPI
- uvicorn
- transformers
- requests
- beautifulsoup4
- sqlite3
- pydantic

## Instalación

1. Clonar el repositorio.:

    ```bash
    git clone https://github.com/Lewis19K/Prozer.git
    cd Prozer
    ```

2. Instalar las dependencias utilizando pip:

    ```bash
    pip install -r requirements.txt
    ```

    Donde `requirements.txt` contiene una lista de las dependencias requeridas.

3. Ejecutar el servidor:

    ```bash
    uvicorn prozer_test:app --reload
    ```

    Este comando iniciará un servidor en el puerto 8000 que puede ser accedido en la dirección `http://localhost:8000/`.

## Probar la API

Gracias a FastAPI se puede acceder a `localhost:8000/docs` para ver la documentación del API y probar los endpoints. Sino, se puede utilizar herramientas como Postman o cURL. Estas son las rutas de los endpoints:

- `/scrape`: Recibe una URL de un sitio de noticias como [elmostrador.cl](https://elmostrador.cl/) y extrae los títulos y descripciones de los artículos de ese sitio.
- `/process`: Recibe un texto y devuelve un resultado de sentimiento de la clasificación de sentimientos de la API de transformers llamada `sentiment-analysis`.
- `/combined`: Recibe una URL de una noticia como las del sitio [elmostrador.cl](https://elmostrador.cl/), realiza scraping de datos y procesa el contenido utilizando un modelo de inteligencia artificial y devuelve el resultado en formato JSON.
