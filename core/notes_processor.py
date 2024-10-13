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


def extract_columns(data: List[Dict], columns: List[str]) -> List[Dict]:
    """
    Extrae las columnas especificadas del conjunto de datos
    """
    return [{col: row[col] for col in columns if col in row} for row in data]
