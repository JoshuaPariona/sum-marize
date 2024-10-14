""" Process notes that come in CSV """

import csv
import chardet  # Para detectar la codificación de los archivos
from typing import List, Dict


def detect_encoding(file_path: str) -> str:
    """
    Detecta la codificación de un archivo CSV.
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def detect_delimiter(sample: str) -> str:
    """
    Detecta el delimitador del archivo CSV usando `csv.Sniffer`.
    """
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(sample)
    return dialect.delimiter


def parse_csv(file_path: str) -> List[Dict]:
    """
    Parsea el contenido del archivo CSV y convierte cada fila en un diccionario con sus columnas.
    Detecta automáticamente el delimitador y la codificación del archivo.
    
    :param file_path: Ruta al archivo CSV.
    :return: Lista de diccionarios con los datos procesados.
    """
    # Detectar la codificación del archivo
    encoding = detect_encoding(file_path)

    with open(file_path, 'r', encoding=encoding) as f:
        sample = f.read(1024)  # Leer una muestra para detectar el delimitador
        f.seek(0)  # Volver al inicio del archivo después de leer la muestra

        # Detectar el delimitador
        delimiter = detect_delimiter(sample)

        # Crear el lector de CSV
        csv_reader = csv.DictReader(f, delimiter=delimiter)
        notes = []

        # Procesar el archivo CSV
        for row in csv_reader:
            cleaned_row = clean_data(row)
            notes.append(cleaned_row)

    return notes


def clean_data(row: Dict) -> Dict:
    """
    Limpia y normaliza los datos del CSV.
    Convierte todos los valores a strings limpios y elimina espacios innecesarios.
    """
    cleaned_row = {key.strip(): value.strip() for key, value in row.items()}
    return cleaned_row
