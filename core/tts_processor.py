import pyttsx3
import hashlib
import json
import io
import os


def hash_json(data):
    json_string = json.dumps(data, sort_keys=True).encode("utf-8")
    hash_object = hashlib.sha256(json_string)
    hash_hex = hash_object.hexdigest()
    return hash_hex


def json_to_text(data) -> str:
    text_output = data["tag"]
    for student in data["data"]:
        text_output += f"\nEstudiante con codigo {student['codigo']}, {student['f-surname']} {student['m-surname']} {student['name']} tiene notas de: Examen Parcial nota de {student['ep']}, Evaluación continua nota de {student['ev']}, Examen final nota de {student['ef']}, Promedio Final nota de {student['pf']}."                                  
    return text_output


async def process_data(data):
    engine = pyttsx3.init()
    engine.setProperty("rate", 130)
    audio_buffer = io.BytesIO()

    engine.save_to_file(json_to_text(data), "students_audio.wav")
    engine.runAndWait()

    with open("students_audio.wav", "rb") as f:
        audio_buffer.write(f.read())
    audio_buffer.seek(0)

    if os.path.exists("students_audio.wav"):
        os.remove("students_audio.wav")

    return audio_buffer
