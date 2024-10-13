""" Process notes that come in PDF """

import pdfplumber
import pandas as pd
import numpy as np
from typing import List, Dict


def parse_pdf_table(file_path: str) -> List[Dict]:
    """
    Extrae tablas de un archivo PDF y convierte cada fila en un diccionario con sus columnas.
    Si la tabla ocupa más de una hoja, une los datos en una sola lista.

    :param file_path: Ruta al archivo PDF.
    :return: Lista de diccionarios con los datos procesados.
    """
    notes = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue  # Salta si no se encuentra una tabla

                # Procesar la tabla
                # Primera fila como encabezados
                headers = [cell.strip() if cell else "" for cell in table[0]]

                # Procesar las filas siguientes (omitiendo la primera que son los encabezados)
                for row in table[1:]:
                    if row:  # Verifica que la fila no esté vacía
                        row_dict = {headers[i]: row[i].strip(
                        ) if row[i] else "" for i in range(len(headers))}
                        # Limpia y normaliza los datos
                        cleaned_row = clean_data(row_dict)
                        notes.append(cleaned_row)

    return notes


def clean_data(row: Dict) -> Dict:
    """
    Limpia y normaliza los datos del PDF, asegurando que los tipos de datos sean compatibles con JSON.
    
    :param row: Diccionario que representa una fila de datos.
    :return: Diccionario limpio y normalizado.
    """
    cleaned_row = {}
    for key, value in row.items():
        if pd.isnull(value):  # Si el valor es NaN, lo manejamos como una cadena vacía
            cleaned_row[key] = ""  # Cambiar a "" para NaN
        elif isinstance(value, (np.int64, np.float64)):
            cleaned_row[key] = value.item()  # Convertir a int o float nativo
        else:
            # Intentar convertir a un número si es posible
            try:
                cleaned_row[key] = int(value) if isinstance(value, (int, float, str)) and str(
                    value).replace('.', '', 1).isdigit() else str(value).strip()
            except (ValueError, TypeError):
                cleaned_row[key] = str(value).strip() if value else ""

    return cleaned_row
