import config
import mimetypes
from typing import List, Dict
from process.csv import parse_csv
from process.excel_v2 import parse_excel
from process.pdf import parse_pdf_table
from process.txt import parse_txt_table


async def process_notes_file(file) -> Dict:
    # Obtener el tipo de archivo basado en la extensión o contenido
    file_type, _ = mimetypes.guess_type(file.filename)

    # Crear una ruta temporal para guardar el archivo
    file_path = f"temp_{file.filename}"

    # Guardar el archivo subido en una ruta temporal
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Identificar y procesar el archivo según su tipo
    if file_type == 'text/csv':
        notes_data = parse_csv(open(file_path, 'r').read())
    elif file_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
        notes_data = parse_excel(file_path)
    elif file_type == 'application/pdf':
        notes_data = parse_pdf_table(file_path)
    elif file_type == 'text/plain':
        notes_data = parse_txt_table(file_path)
    else:
        raise ValueError(f"Tipo de archivo no soportado: {file_type}")

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


def extract_columns_v2(data: List[Dict], columns: List[str]) -> List[Dict]:
    """
    Extrae las columnas especificadas del conjunto de datos
    """
    return [{col: row[col] for col in columns if col in row} for row in data]


def extract_columns(data: List[Dict], column_types: List[str]) -> List[Dict]:
    """
    Extrae las columnas especificadas del conjunto de datos usando palabras clave.

    :param data: Lista de diccionarios con los datos procesados.
    :param column_types: Lista de tipos de columnas que deseas extraer (ej: "Código Alumno", "Apellidos y Nombres", "NP").
    :return: Lista de diccionarios solo con las columnas especificadas.
    """
    # Mapear las columnas de los datos a las palabras clave correspondientes
    mapped_columns = {}

    if not data:
        return []

    # Obtener los nombres reales de las columnas en el dataset
    first_row = data[0]

    for column_type in column_types:
        # Buscar las columnas que coincidan con las palabras clave definidas en config.keywords
        matched = False
        for actual_column in first_row.keys():
            # Validar que actual_column no sea None antes de aplicar .lower()
            if actual_column and any(keyword.lower() in actual_column.lower() for keyword in config.keywords[column_type]):
                mapped_columns[column_type] = actual_column
                matched = True
                break

        # Si no se encontró coincidencia, asignar una columna vacía
        if not matched:
            # Indicar que no se encontró una columna
            mapped_columns[column_type] = None

    # Extraer solo las columnas mapeadas
    extracted_data = []
    for row in data:
        new_row = {}
        for col_type, actual_col in mapped_columns.items():
            if actual_col is not None and actual_col in row:
                new_row[col_type] = row[actual_col]
            else:
                # Asignar valor vacío si no se encontró columna
                new_row[col_type] = ""
        extracted_data.append(new_row)

    return extracted_data
