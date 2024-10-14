import csv
import openai
import os

from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

SECRET_KEY = os.getenv('KEY_API_OPENAI')
_api_key = SECRET_KEY
openai.api_key = _api_key

# Palabras clave predeterminadas y opcionales
keywords = {"Código Alumno", "Apellidos y Nombres", "NP", "EV", "NF"}
optional_keywords = {
    "NP": ["Nota Parcial", "nota parcial", "notaParcial"],
    "EV": ["Evaluación Continua"],
    "NF": ["Nota Final"]
}


def call_openai_for_mapping(headers: List[str]) -> Dict[str, str]:
    """
    Llama a la API de OpenAI para mapear encabezados a las palabras clave más relevantes.
    """
    prompt = f"""
    Tengo los siguientes encabezados de un archivo CSV: {headers}. 
    Relaciónalos con las siguientes palabras clave: ['Código Alumno', 'Apellidos y Nombres', 'NP', 'EV', 'NF']. 
    Si algún encabezado no coincide directamente, intenta sugerir cuál palabra clave podría corresponder o indícame "Sin Coincidencia".
    """

    mensaje = [
        {"role": "system", "content": "Eres un asistente que mapea encabezados de CSV."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usa gpt-4 si tienes acceso
            messages=mensaje,
            max_tokens=150,
            temperature=0.5
        )

        # Procesar la respuesta
        mapping_suggestion = response['choices'][0]['message']['content'].strip()

        # Intentar convertir el texto en un diccionario
        try:
            mapping_dict = eval(mapping_suggestion)
        except:
            mapping_dict = {}  # Manejo de errores si eval no puede parsear la respuesta correctamente

        return mapping_dict

    except Exception as e:
        print(f"Error llamando a OpenAI: {e}")
        return {}


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
    Este método no usa OpenAI y trata de mapear palabras clave opcionales si no se encuentran las predeterminadas.
    """
    csv_reader = csv.DictReader(contents.splitlines())
    notes = []

    # Procesa el CSV y trata de mapear palabras clave opcionales si no se encuentran las predeterminadas
    for row in csv_reader:
        cleaned_row = clean_data_2(row)
        if not all(keyword in cleaned_row for keyword in keywords):
            # Mapear palabras clave opcionales si no se encuentran las exactas
            cleaned_row = match_optional_keywords(cleaned_row, optional_keywords)
        notes.append(cleaned_row)
    
    return notes


def clean_data_2(row: Dict) -> Dict:
    """
    Limpia y normaliza los datos del CSV.
    """
    return {key.strip(): value.strip() for key, value in row.items()}


def clean_data(row: Dict, mapping: Dict) -> Dict:
    """
    Limpia y normaliza los datos del CSV, y los mapea a las palabras clave utilizando OpenAI.
    """
    cleaned_row = {mapping.get(key, key): value.strip() for key, value in row.items()}
    return cleaned_row


def match_optional_keywords(row: Dict, optional_keywords: Dict) -> Dict:
    """
    Intenta mapear palabras clave opcionales relacionadas.
    """
    for key, related_keywords in optional_keywords.items():
        for related_key in related_keywords:
            if related_key in row:
                row[key] = row.pop(related_key)
    return row
