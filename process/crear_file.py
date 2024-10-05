""" Crear las notas de los alumnos """
import pandas as pd
from faker import Faker
import os  # Importa la librería os para crear directorios

fake = Faker()

# Crear listas para almacenar los datos
codigos_alumnos = []
apellidos_nombres = []
np = []
ev = []
nf = []

# Generar datos para 90 alumnos
for _ in range(90):
    codigo_alumno = str(fake.random_int(
        min=100000, max=999999))  # Código de 6 dígitos
    codigos_alumnos.append(codigo_alumno)  # Agrega a la lista
    apellidos_nombres.append(fake.name())
    np.append(fake.random_int(min=0, max=20))  # Nota Parcial
    ev.append(fake.random_int(min=0, max=10))  # Evaluación Continua
    nf.append(fake.random_int(min=0, max=20))  # Nota Final

# Crear un DataFrame de pandas
df = pd.DataFrame({
    'Código Alumno': codigos_alumnos,
    'Apellidos y Nombres': apellidos_nombres,
    'NP': np,
    'EV': ev,
    'NF': nf
})

# Crear la carpeta res si no existe
os.makedirs('/res', exist_ok=True)

# Guardar el DataFrame como un archivo CSV
ruta = r'H:\Major\Hachaton\sum-marize\res\alumnos_notas.csv'
df.to_csv(ruta, index=False)

print("Archivo CSV creado exitosamente: alumnos.csv")
