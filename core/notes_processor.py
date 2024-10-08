from typing import List, Dict
from process.csv import parse_csv


async def process_notes_file(file) -> Dict:
    # Leer el contenido del archivo CSV
    contents = await file.read()

    # Procesar el CSV, limpiar y analizar
    notes_data = parse_csv(contents.decode("utf-8"))

    # Convertir los datos procesados en las diferentes formas de JSON
    processed_notes = {
        "complete": notes_data,
        "np_only": extract_columns(notes_data, ["Código Alumno", "Apellidos y Nombres", "NP"]),
        "ev_only": extract_columns(notes_data, ["Código Alumno", "Apellidos y Nombres", "EV"]),
        "nf_only": extract_columns(notes_data, ["Código Alumno", "Apellidos y Nombres", "NF"]),
        "np_ev_combined": extract_columns(notes_data, ["Código Alumno", "Apellidos y Nombres", "NP", "EV"]),
        "ev_nf_combined": extract_columns(notes_data, ["Código Alumno", "Apellidos y Nombres", "EV", "NF"]),
        "np_nf_combined": extract_columns(notes_data, ["Código Alumno", "Apellidos y Nombres", "NP", "NF"])
    }

    return processed_notes


def extract_columns(data: List[Dict], columns: List[str]) -> List[Dict]:
    # Extrae las columnas especificadas del conjunto de datos
    return [{col: row[col] for col in columns if col in row} for row in data]
