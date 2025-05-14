from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt

# Configura la conexión a Elasticsearch Cloud
client = Elasticsearch(
    "https://591fd63ecbb34d09a7050c1f828859e3.us-central1.gcp.cloud.es.io:443",
    api_key="T0VKWHpaWUI0ZDJETF9GcWU2OTQ6cEFLSF8tRFlwMUFxaVFyMVBFWUVyUQ=="
)

# Nombre del índice
index_name = "search-g9n3"

try:
    # Consulta para obtener todos los datos (ajústala si necesitas filtrar)
    query = {"query": {"match_all": {}}}
    response = client.search(index=index_name, body=query, size=10000) # Ajusta 'size' si tienes más de 10,000 documentos

    # Procesa los resultados en un DataFrame de Pandas
    data = [hit['_source'] for hit in response['hits']['hits']]
    df = pd.DataFrame(data)

    # *** ¡Aquí debes seleccionar y adaptar las columnas para tu gráfica! ***

    # Ejemplo 1: Gráfico de barras de la frecuencia de una columna categórica (ej. 'genero')
    columna_categorica = "SEXO"
    frecuencia_genero = df[columna_categorica].value_counts()
    plt.figure(figsize=(8, 6))
    frecuencia_genero.plot(kind='bar')
    plt.title(f"Frecuencia de {columna_categorica}")
    plt.xlabel(columna_categorica)
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=0)
    nombre_archivo_grafica_genero = "frecuencia_genero.png"
    plt.savefig(nombre_archivo_grafica_genero)
    print(f"Gráfica guardada como '{nombre_archivo_grafica_genero}'.")
    plt.close()


    #Histograma de Edades
    columna_edad = "EDAD"
    # Asegúrate de convertir la columna a numérica si es necesario
    df['EDAD'] = pd.to_numeric(df['EDAD'], errors='coerce')
    df_edad_valida = df.dropna(subset=['EDAD']) # Eliminar valores no numéricos

    plt.figure(figsize=(10, 6))
    plt.hist(df_edad_valida['EDAD'], bins=15, edgecolor='black')
    plt.title("Distribución de Edades")
    plt.xlabel("Edad")
    plt.ylabel("Frecuencia")
    nombre_archivo_grafica_edad = "histograma_edad.png"
    plt.savefig(nombre_archivo_grafica_edad)
    print(f"Gráfica guardada como '{nombre_archivo_grafica_edad}'.")
    plt.close()

    #Gráfico de Barras Apiladas de Consumo de Sustancias por Género (Ejemplo con Alcohol y Tabaco)
    sustancias = ["ALCOHOL", "TABACO"]
    df_sustancias_genero = df.groupby('SEXO')[sustancias].sum()
    df_sustancias_genero.plot(kind='bar', stacked=True, figsize=(8, 6))
    plt.title("Consumo de Alcohol y Tabaco por Género")
    plt.xlabel("Género")
    plt.ylabel("Cantidad de Casos")
    plt.xticks(rotation=0)
    plt.legend(title="Sustancia")
    nombre_archivo_grafica_sustancias_genero = "sustancias_por_genero.png"
    plt.savefig(nombre_archivo_grafica_sustancias_genero)
    print(f"Gráfica guardada como '{nombre_archivo_grafica_sustancias_genero}'.")
    plt.close()

    # Ejemplo 2: Histograma de una columna numérica (ej. 'edad' - si tuvieras esa columna)
    # columna_numerica = "edad"
    # plt.figure(figsize=(8, 6))
    # plt.hist(df[columna_numerica], bins=10, edgecolor='black')
    # plt.title(f"Distribución de {columna_numerica}")
    # plt.xlabel(columna_numerica)
    # plt.ylabel("Frecuencia")
    # nombre_archivo_grafica_edad = "histograma_edad.png"
    # plt.savefig(nombre_archivo_grafica_edad)
    # print(f"Gráfica guardada como '{nombre_archivo_grafica_edad}'.")
    # plt.close()

    # *** ¡Añade aquí más ejemplos de gráficas según tus necesidades! ***

except Exception as e:
    print(f"Ocurrió un error al graficar los datos: {e}")