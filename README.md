# sum-marize

# Proyecto Hackathon: Automatización de la Subida de Notas

## Descripción del Proyecto

Este proyecto fue desarrollado para la **Hackathon de la Facultad de Ingeniería de Sistemas e Informática** de la *Universidad Nacional Mayor de San Marcos* con el objetivo de automatizar un proceso administrativo clave: la **subida de notas al sistema SUM**. Actualmente, muchos profesores enfrentan problemas debido a la complejidad, demora y manualidad del proceso, lo que genera retrasos y errores. Nuestra solución propone una plataforma que automatiza la carga de notas, simplificando y optimizando el proceso.

## Problema a Resolver

La gestión de notas en el sistema **SUM** es un proceso manual y tedioso, que se agrava por la gran cantidad de estudiantes y las múltiples responsabilidades de los profesores. Además, algunos docentes que no están familiarizados con herramientas digitales encuentran dificultades, lo que genera demoras y riesgo de errores. Los pasos actuales incluyen:

1. Ingreso al SUM.
2. Selección de la opción "Ingreso de calificaciones".
3. Carga manual de cada nota (parcial, evaluación continua y nota final).
4. Validación y grabación.

Este proceso es propenso a errores, sobre todo si no se completa dentro del tiempo permitido por el sistema, provocando retrasos en la publicación de notas.

## Solución Propuesta

Nuestra plataforma automatiza el proceso de subida de notas mediante el uso de **machine learning** y herramientas de procesamiento de archivos. La solución permite a los profesores cargar documentos de notas en múltiples formatos (CSV, Excel) para procesar las calificaciones de manera rápida y precisa. La innovación adicional incluye la integración de tecnología de **texto a voz** para que los profesores puedan escuchar el proceso de llenado automático, asegurando una revisión completa y reduciendo los errores.

### Funcionalidades Principales:

- **Carga de archivos:** Los profesores pueden subir archivos de notas en formatos como **CSV** y **Excel**.
- **Procesamiento automático:** El sistema procesa los archivos, mapea las notas y las carga en el sistema SUM sin intervención manual.
- **Validación de datos:** Los datos se verifican antes de ser enviados al SUM, garantizando la precisión.
- **Revisión con texto a voz:** Se puede escuchar la revisión de las notas para mayor seguridad.

## Innovación

Este proyecto destaca por el uso de tecnologías de última generación para la automatización de un proceso administrativo:

- **Microservicios**: La arquitectura está basada en microservicios utilizando **FastAPI**, lo que permite que el sistema sea escalable y fácil de integrar con otros sistemas.
- **Machine Learning**: Hemos implementado un modelo de **Random Forest Classifier** con **scikit-learn** para predecir y clasificar los datos correctamente.
- **Interfaz Interactiva**: Utilizamos **React** para el frontend, brindando una experiencia intuitiva y amigable para los usuarios.
- **Procesamiento de Archivos**: Utilizamos herramientas como **openpyxl** para la lectura y manejo eficiente de archivos **Excel**, y **módulos de Python** para el procesamiento de **CSV**.
- **Texto a Voz**: Implementamos un sistema de revisión de notas mediante **texto a voz** para que los profesores puedan escuchar el llenado automático y realizar correcciones si es necesario.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal para el desarrollo del backend.
- **FastAPI**: Framework para la creación de APIs y microservicios.
- **React**: Framework de frontend para crear la interfaz interactiva.
- **CSV** y **openpyxl**: Para el procesamiento de archivos.
- **scikit-learn**: Para el desarrollo y entrenamiento del modelo de machine learning.
- **Visual Studio Code**: IDE utilizado para el desarrollo.
- **Uvicorn**: Servidor ASGI para la ejecución de la API.

## Instalación y Ejecución

### Requisitos

- Python 3.9+
- Node.js y npm
- Paquetes de Python: `FastAPI`, `pandas`, `openpyxl`, `scikit-learn`, `uvicorn`
- Paquetes de Node.js: `react`, `vite`

### Instrucciones

1. Clona el repositorio:

   ```bash
   git clone <repo-url>
   ```
2. Instala las dependencias de Python:

   ```bash
   pip install -r requirements.txt
   ```
3. Instala las dependencias de Node.js:

   ```bash
   npm install
   ```
4. Ejecuta el servidor de backend:

   ```bash
   uvicorn main:app --reload
   ```
5. Ejecuta el frontend: [https://github.com/JoshuaPariona/sum-marize-app.git]()

   ```bash
   npm run dev
   ```
6. Accede a la aplicación en `http://localhost:3000`.

## Contribuidores

- **Equipo de la Facultad de Ingeniería de Sistemas e Informática**
  - Max B. Saavedra: [www.linkedin.com/in/max-saavedra]()
  - Fabricio V. Chuquispuma :  [https://www.linkedin.com/in/fabriciochuquispuma/]()
  - Valery A. Delgado : [linkedin.com/in/valery-andrea-delgado-de-la-cruz-119a6a2bb]()
  - Joshua B. Pariona : [https://www.linkedin.com/in/joshua-bryan-pariona-santiago-7a808727b/]()

---

Este proyecto fue creado con el propósito de optimizar los procesos administrativos en la universidad, ahorrando tiempo y esfuerzo tanto a docentes como a personal administrativo.
