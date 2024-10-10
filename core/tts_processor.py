import pyttsx3
import hashlib
import json
import io


def hash_json(data):
    json_string = json.dumps(data, sort_keys=True).encode("utf-8")
    hash_object = hashlib.sha256(json_string)
    hash_hex = hash_object.hexdigest()
    return hash_hex


def json_to_text(data) -> str:
    text_output = data["tag"]
    for student in data["data"]:
        text_output += f"\nEstudiante con codigo {student['codigo']}, {student['name']} {student['f-surname']} {student['m-surname']} tiene una nota de {student['grade']}."
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

    return audio_buffer
