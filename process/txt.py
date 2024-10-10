""" Process notes that come in TXT """

import openai
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

SECRET_KEY = os.getenv('KEY_API_OPENAI')

# Clave de OpenAI
_api_key = SECRET_KEY

openai.api_key = _api_key

keywords = {"Código Alumno", "Apellidos y Nombres", "NP", "EV", "NF"}


def call_openai_for_mapping(headers: List[str]) -> Dict[str, str]:
    """
    Llama a la API de OpenAI para mapear encabezados a las palabras clave más relevantes usando la nueva API.
    """
    prompt = f"""
    Tengo los siguientes encabezados de una tabla en un archivo de texto: {headers}. 
    Relaciónalos con las siguientes palabras clave: ['Código Alumno', 'Apellidos y Nombres', 'NP', 'EV', 'NF']. 
    Si algún encabezado no coincide directamente, intenta sugerir cuál palabra clave podría corresponder o indícame "Sin Coincidencia".
    """

    mensaje = [
        {"role": "system", "content": "Eres un asistente que mapea encabezados de tablas en archivos de texto."},
        {"role": "user", "content": prompt}
    ]

    try:
        # Usar la nueva API ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # O usa gpt-4 si tienes acceso
            messages=mensaje,
            max_tokens=150,
            temperature=0.5
        )

        # Procesar la respuesta
        mapping_suggestion = response['choices'][0]['message']['content'].strip(
        )

        # Intentar convertir el texto en un diccionario (ajusta según el formato de respuesta)
        try:
            mapping_dict = eval(mapping_suggestion)
        except:
            mapping_dict = {}  # Manejo de errores si eval no puede parsear la respuesta correctamente

        return mapping_dict

    except Exception as e:
        print(f"Error llamando a OpenAI: {e}")
        return {}


def parse_txt_table(file_path: str) -> List[Dict]:
    """
    Extrae datos tabulares de un archivo TXT y convierte cada fila en un diccionario con sus columnas.
    """
    notes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Detectar la tabla: vamos a suponer que las primeras líneas contienen los encabezados
    # Asumiendo que la primera línea tiene los encabezados
    headers = [header.strip() for header in lines[0].split()]

    # Llama a OpenAI para mapear los encabezados a las palabras clave
    header_mapping = call_openai_for_mapping(headers)

    # Procesar cada línea subsiguiente como una fila de la tabla
    for line in lines[1:]:
        # Separar los valores por espacios (ajusta si los valores están separados por comas, tabs, etc.)
        values = line.split()
        row_dict = {headers[i]: values[i].strip() if i < len(
            values) else "" for i in range(len(headers))}
        cleaned_row = clean_data(row_dict, header_mapping)
        notes.append(cleaned_row)

    return notes


def clean_data(row: Dict, mapping: Dict) -> Dict:
    """
    Limpia y normaliza los datos extraídos del TXT, y los mapea a las palabras clave utilizando OpenAI.
    """
    cleaned_row = {mapping.get(key, key): value.strip(
    ) if value else "" for key, value in row.items()}
    return cleaned_row
