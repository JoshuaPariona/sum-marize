""" Process notes that come in EXCEL """

import openai
import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Dict

# Cargar las variables de entorno
load_dotenv()

SECRET_KEY = os.getenv('KEY_API_OPENAI')
openai.api_key = SECRET_KEY

keywords = {"Código Alumno", "Apellidos y Nombres", "NP", "EV", "NF"}


def call_openai_for_mapping(headers: List[str]) -> Dict[str, str]:
    """
    Llama a la API de OpenAI para mapear encabezados a las palabras clave más relevantes usando la nueva API.
    """
    prompt = f"""
    Tengo los siguientes encabezados de un archivo Excel: {headers}. 
    Relaciónalos con las siguientes palabras clave: ['Código Alumno', 'Apellidos y Nombres', 'NP', 'EV', 'NF']. 
    Si algún encabezado no coincide directamente, intenta sugerir cuál palabra clave podría corresponder o indícame "Sin Coincidencia".
    """

    mensaje = [
        {"role": "system", "content": "Eres un asistente que mapea encabezados de Excel."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=mensaje,
            max_tokens=150,
            temperature=0.5
        )
        mapping_suggestion = response['choices'][0]['message']['content'].strip(
        )

        try:
            mapping_dict = eval(mapping_suggestion)
        except:
            mapping_dict = {}

        return mapping_dict

    except Exception as e:
        print(f"Error llamando a OpenAI: {e}")
        return {}


def detect_headers_with_keywords(df: pd.DataFrame, keywords: List[str]) -> Dict[str, int]:
    """
    Detecta las cabeceras en el DataFrame buscando palabras clave conocidas.
    Devuelve un diccionario con los nombres de las cabeceras y su índice de columna.
    """
    for index, row in df.iterrows():
        for col_idx, cell in enumerate(row):
            if isinstance(cell, str):
                # Si encontramos una palabra clave en la celda
                if any(keyword.lower() in cell.lower() for keyword in keywords):
                    # Identificamos que esta fila contiene las cabeceras
                    headers = {df.columns[col_idx + i]: col_idx + i for i in range(len(
                        row)) if col_idx + i < len(df.columns) and pd.notna(df.iloc[index, col_idx + i])}
                    return headers, index

    return {}, None


def parse_excel(file_path: str) -> List[Dict]:
    """
    Parsea el contenido del archivo Excel y convierte cada fila en un diccionario con sus columnas.
    """
    # Cargar el archivo Excel con pandas
    df = pd.read_excel(file_path, sheet_name=0)

    # Definir las palabras clave de las cabeceras
    header_keywords = ["Código Alumno",
                       "Apellidos y Nombres", "NP", "EV", "NF"]

    # Detectar los encabezados usando palabras clave
    headers, header_row = detect_headers_with_keywords(df, header_keywords)

    if not headers:
        raise ValueError(
            "No se pudieron detectar las cabeceras en el archivo Excel.")

    # Llamar a OpenAI para mapear los encabezados a las palabras clave
    header_mapping = call_openai_for_mapping(list(headers.keys()))

    # Comprobar si el número de encabezados mapeados es menor que las columnas reales
    mapped_columns = [header_mapping.get(col, col) for col in headers.keys()]
    if len(mapped_columns) < len(df.columns):
        # Completar las columnas restantes con sus nombres originales si no fueron mapeadas
        mapped_columns.extend(df.columns[len(mapped_columns):])

    # Extraer la tabla a partir de la fila de los encabezados
    table_data = df.iloc[header_row + 1:].copy()
    table_data.columns = mapped_columns

    # Convertir los datos a una lista de diccionarios
    notes = table_data.dropna(how="all").to_dict(orient="records")

    return notes


def clean_data(row: Dict, mapping: Dict) -> Dict:
    """
    Limpia y normaliza los datos del Excel, y los mapea a las palabras clave utilizando OpenAI.
    """
    cleaned_row = {mapping.get(key, key): str(
        value).strip() if value else "" for key, value in row.items()}
    return cleaned_row
