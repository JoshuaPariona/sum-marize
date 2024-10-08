""" Process notes that come in CSV """

import csv
import openai
import os

from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

# Clave de OpenAI
_api_key = 'api'

openai.api_key = _api_key

keywords = {"Código Alumno", "Apellidos y Nombres", "NP", "EV", "NF"}


def call_openai_for_mapping(headers: List[str]) -> Dict[str, str]:
    """
    Llama a la API de OpenAI para mapear encabezados a las palabras clave más relevantes usando la nueva API.
    """
    prompt = f"""
    Tengo los siguientes encabezados de un archivo CSV: {headers}. 
    Relaciónalos con las siguientes palabras clave: ['Código Alumno', 'Apellidos y Nombres', 'NP', 'EV', 'NF']. 
    Si algún encabezado no coincide directamente, intenta sugerir cuál palabra clave podría corresponder o indícame "Sin Coincidencia".
    """

    # Usar la nueva API ChatCompletion
    response = openai.completions.create(
        model="gpt-3.5-turbo",  # O usa gpt-4 si tienes acceso
        prompt=[
            {"role": "system", "content": "Eres un asistente que mapea encabezados de CSV."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.5
    )

    # Procesar la respuesta
    mapping_suggestion = response['choices'][0]['message']['content'].strip()

    # Intentar convertir el texto en un diccionario (ajusta según el formato de respuesta)
    try:
        mapping_dict = eval(mapping_suggestion)
    except:
        mapping_dict = {}  # Maneja el error si eval no puede parsear la respuesta correctamente

    return mapping_dict


def parse_csv(contents: str) -> List[Dict]:
    """
    Parsea el contenido del CSV y convierte cada fila en un diccionario con sus columnas.
    """
    csv_reader = csv.DictReader(contents.splitlines())
    headers = csv_reader.fieldnames  # Obtiene los encabezados del CSV

    # Llama a OpenAI para mapear los encabezados a las palabras clave
    header_mapping = call_openai_for_mapping(headers)

    notes = []

    # Procesa el CSV con los encabezados mapeados
    for row in csv_reader:
        cleaned_row = clean_data(row, header_mapping)
        notes.append(cleaned_row)

    return notes


def parse_csv_2(contents: str) -> List[Dict]:
    """
    Parsea el contenido del CSV y convierte cada fila en un diccionario con sus columnas.
    """
    csv_reader = csv.DictReader(contents.splitlines())
    notes = []

    keywords = {"Código Alumno", "Apellidos y Nombres", "NP", "EV", "NF"}
    optional_keywords = {"NP": ["Nota Parcial", "nota parcial", "notaParcial"], "EV": [
        "Evaluación Continua"], "NF": ["Nota Final"]}

    # Procesa el CSV, si no se encuentran las palabras clave exactas, usa las aproximadas
    for row in csv_reader:
        cleaned_row = clean_data_2(row)
        # Verifica si todas las palabras clave existen
        if not all(keyword in cleaned_row for keyword in keywords):
            # Si no, buscar palabras relacionadas
            cleaned_row = match_optional_keywords(
                cleaned_row, optional_keywords)
        notes.append(cleaned_row)
    return notes


def clean_data_2(row: Dict) -> Dict:
    """
    Limpia y normaliza los datos del CSV
    """
    return {key.strip(): value.strip() for key, value in row.items()}


def clean_data(row: Dict, mapping: Dict) -> Dict:
    """
    Limpia y normaliza los datos del CSV, y los mapea a las palabras clave utilizando OpenAI
    """
    cleaned_row = {mapping.get(key, key): value.strip()
                   for key, value in row.items()}
    return cleaned_row


def match_optional_keywords(row: Dict, optional_keywords: Dict) -> Dict:
    """
    Intenta mapear palabras clave opcionales relacionadas
    """
    for key, related_keywords in optional_keywords.items():
        for related_key in related_keywords:
            if related_key in row:
                row[key] = row.pop(related_key)
    return row
