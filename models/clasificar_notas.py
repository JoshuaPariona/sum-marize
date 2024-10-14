import pandas as pd
import numpy as np
from faker import Faker
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Paso 1: Preparar los datos


def prepare_data(notes_df):
    """
    Prepara los datos para entrenar el modelo de clasificación.
    Calcula la nota final ponderada y genera la columna 'aprobado'.
    """
    # Calcular el resultado final basado en la fórmula
    notes_df['resultado_final'] = (
        0.2 * notes_df['NP'] + 0.6 * notes_df['EV'] + 0.2 * notes_df['NF']).round()

    print(notes_df['resultado_final'])

    # Determinar si aprueba o no (1 = aprueba, 0 = reprueba)
    notes_df['aprobado'] = np.where(notes_df['resultado_final'] >= 11, 1, 0)

    # Seleccionar las características para entrenar el modelo (NP, EV, NF)
    X = notes_df[['NP', 'EV', 'NF']]
    y = notes_df['aprobado']

    return X, y

# Paso 2: Entrenar el modelo


def train_model(X, y):
    """
    Entrena el modelo de clasificación con RandomForestClassifier.
    """
    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Hacer predicciones y verificar la precisión
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Precisión del modelo: {accuracy * 100:.2f}%')

    return model

# Paso 3: Guardar el modelo entrenado


def save_model(model, model_path='classification_model.pkl'):
    """
    Guarda el modelo entrenado en un archivo .pkl
    """
    joblib.dump(model, model_path)
    print(f'Modelo guardado en {model_path}')

# Paso 4: Cargar el modelo para usar en predicciones


def load_model(model_path='classification_model.pkl'):
    """
    Carga el modelo entrenado desde el archivo .pkl
    """
    model = joblib.load(model_path)
    return model


# Ejemplo de cómo entrenar y guardar el modelo
if __name__ == "__main__":

    fake = Faker()

    # Crear un dataframe de ejemplo con las notas
    data = {
        'NP': [10, 12, 9, 14, 8, 15, 16, 11, 7, 18],
        'EV': [12, 15, 10, 14, 9, 13, 14, 12, 8, 16],
        'NF': [11, 13, 8, 15, 9, 14, 12, 11, 7, 17]
    }

    # Generar más datos
    for _ in range(1000):  # Genera 1000 filas adicionales
        data['NP'].append(fake.random_int(min=0, max=20))
        data['EV'].append(fake.random_int(min=0, max=20))
        data['NF'].append(fake.random_int(min=0, max=20))

    notes_df = pd.DataFrame(data)

    # Preparar los datos
    X, y = prepare_data(notes_df)

    # Entrenar el modelo
    model = train_model(X, y)

    # Guardar el modelo entrenado
    save_model(model)
