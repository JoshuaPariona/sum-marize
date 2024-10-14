""" Process notes that come in PDF """

import pdfplumber
import pandas as pd
from typing import List, Dict

# Definición de palabras clave
keywords = {
    "Código Alumno": [
        "codigo alumno", "código alumno", "código de alumno", "codigo de alumno",
        "código estudiantil", "clave de alumno", "matrícula de alumno",
        "identificación de alumno", "número de alumno", "carnet de alumno",
        "student code", "student id", "student number", "student identification"
    ],
    "Apellidos y Nombres": [
        "apellidos y nombres", "nombre completo", "nombres completos", "nombre y apellidos",
        "last names and first names", "full name"
    ],
    "NP": [
        "nota parcial", "puntuación parcial", "evaluación parcial"
    ],
    "EV": [
        "evaluación continua", "trabajo en clase", "evaluación formativa"
    ],
    "NF": [
        "nota final", "calificación final", "puntuación final", "evaluación sumativa"
    ]
}


def parse_pdf_table(file_path: str) -> List[Dict]:
    """
    Extrae tablas de un archivo PDF y convierte cada fila en un diccionario con sus columnas.
    Si la tabla ocupa más de una hoja, une los datos en una sola lista.

    :param file_path: Ruta al archivo PDF.
    :return: Una lista de diccionarios que incluye todos los datos procesados.
    """
    notes = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue  # Salta si no se encuentra una tabla

                # Procesar la tabla
                headers = [cell.strip() if cell else "" for cell in table[0]]
                header_mapping = map_headers(headers)

                # Procesa las filas siguientes (omitiendo la primera que son los encabezados)
                for row in table[1:]:
                    if row:  # Verifica que la fila no esté vacía
                        row_dict = process_row(row, header_mapping)
                        if row_dict:  # Solo agrega si hay datos
                            notes.append(row_dict)

    return notes


def map_headers(headers: List[str]) -> Dict[str, str]:
    """
    Mapea los encabezados de la tabla a las palabras clave definidas.

    :param headers: Lista de encabezados extraídos.
    :return: Un diccionario que relaciona cada encabezado con su clave correspondiente.
    """
    header_mapping = {}
    for i, header in enumerate(headers):
        for key, variants in keywords.items():
            if any(variant.lower() in header.lower() for variant in variants):
                header_mapping[i] = key  # Guardamos el índice del encabezado
                break
    return header_mapping


def process_row(row: List[str], header_mapping: Dict[int, str]) -> Dict[str, str]:
    """
    Procesa cada fila y asigna los valores a las columnas correspondientes.

    :param row: Lista de valores en la fila.
    :param header_mapping: Mapa de encabezados a palabras clave.
    :return: Diccionario con los datos de la fila organizados por palabras clave.
    """
    row_dict = {}
    for index, value in enumerate(row):
        if index in header_mapping:  # Solo asigna si el índice está en el mapeo
            row_dict[header_mapping[index]] = value.strip() if value else ""

    return row_dict
