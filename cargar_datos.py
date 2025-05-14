from elasticsearch import Elasticsearch
import pandas as pd

client = Elasticsearch(
    "https://591fd63ecbb34d09a7050c1f828859e3.us-central1.gcp.cloud.es.io:443",
    api_key="T0VKWHpaWUI0ZDJETF9GcWU2OTQ6cEFLSF8tRFlwMUFxaVFyMVBFWUVyUQ=="
)

index_name = "search-g9n3"

# Definir el mapping (puedes ajustarlo según tus columnas)
mappings = {
    "properties": {
        "id_paciente": {"type": "keyword"},
        "nombre": {"type": "text"},
        "fecha_nacimiento": {"type": "date"},
        "genero": {"type": "keyword"},
        # ... añade los mappings para el resto de tus columnas ...
    }
}

# Crear el índice con el mapping si no existe
if not client.indices.exists(index=index_name):
    create_index_response = client.indices.create(index=index_name, mappings=mappings)
    print("Índice creado:", create_index_response)
else:
    print(f"El índice '{index_name}' ya existe.")

# Ruta a tu archivo de datos
ruta_archivo = r"D:\aldah\Documents\Tuxxter_Elasticsearch\CIJ_Pacientes.csv"

try:
    # Lee el dataset
    df = pd.read_csv(ruta_archivo)

    # Itera sobre las filas del DataFrame y las indexa en Elasticsearch
    for index, row in df.iterrows():
        documento = row.to_dict()
        client.index(index=index_name, document=documento)  # ¡Corregido aquí!

    print(f"Se cargaron {len(df)} documentos al índice '{index_name}'.")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta: {ruta_archivo}")
except Exception as e:
    print(f"Ocurrió un error: {e}")

# Ya no es necesario llamar a put_mapping aquí si creaste el índice con el mapping
# mapping_response = client.indices.put_mapping(index=index_name, body=mappings)
# print(mapping_response)