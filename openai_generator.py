import openai
import os

openai.api_key = 'sk-proj-SmmISqBO3ESPvfghaCvtT3BlbkFJJF4lGtBH3R7LM841VDM8'

def generar_informacion(tema, objetivo_general, objetivo_antes):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Generar un resumen en HTML de menos de 100 palabras educativo sobre {tema} que cumpla con los objetivos: {objetivo_general} y {objetivo_antes}. El resumen debe ser para el curso Estructura de Datos."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar información: {e}")

def generar_video_youtube(tema):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Buscar un enlace de YouTube en HTML que tenga un video educativo relevante sobre {tema}. Solo debes generar el enlace y nada más."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar enlace de video: {e}")

def generar_objetivos_clase(tema, objetivo_general, objetivo_antes):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Generar una lista en HTML de objetivos de aprendizaje claros y específicos para una clase sobre {tema}. Los objetivos deben alinearse con los siguientes objetivos: {objetivo_general} y {objetivo_antes}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar objetivos de la clase: {e}")

def generar_preguntas_motivacion(tema, objetivo_general, objetivo_antes):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Generar tres preguntas en HTML de motivación que se pueden hacer a los estudiantes al inicio de una clase sobre {tema}. Las preguntas deben despertar el interés y la curiosidad de los estudiantes sobre el tema. Objetivos: {objetivo_general} y {objetivo_antes}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar preguntas de motivación: {e}")

def generar_cuestionario(tema, objetivo_general, objetivo_antes):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Generar un cuestionario en HTML con cinco preguntas de opción múltiple sobre {tema}. Cada pregunta debe tener cuatro opciones de respuesta, incluyendo una correcta. Objetivos: {objetivo_general} y {objetivo_antes}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar cuestionario: {e}")

def generar_motivacion(tema, objetivo_general, objetivo_antes):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Escribir un párrafo en HTML motivacional que explique la importancia de estudiar {tema} y cómo puede beneficiar a los estudiantes en su carrera de Ingeniería de Computación y Sistemas. Objetivos: {objetivo_general} y {objetivo_antes}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar motivación: {e}")

def generar_contenido_clase(tema, objetivo_general, objetivo_durante):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Proveer un esquema en HTML detallado del contenido que se debe cubrir durante una clase sobre {tema}. Incluir los puntos clave y ejemplos relevantes. Objetivos: {objetivo_general} y {objetivo_durante}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar contenido de clase: {e}")

def generar_ejercicios_programacion(tema, objetivo_general, objetivo_durante):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Crear tres ejercicios de programación en HTML que los estudiantes puedan realizar durante la clase para practicar el tema {tema}. Cada ejercicio debe incluir una descripción del problema y los requisitos. Objetivos: {objetivo_general} y {objetivo_durante}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar ejercicios de programación: {e}")

def generar_ejemplos_casos_reales(tema, objetivo_general, objetivo_durante):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Proporcionar dos ejemplos en HTML de la vida real que demuestren la aplicación práctica del tema {tema} en el campo de la computación y los sistemas. Objetivos: {objetivo_general} y {objetivo_durante}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar ejemplos con casos reales: {e}")

def generar_trabajo_grupal(tema, objetivo_general, objetivo_durante):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Describir una actividad en HTML de trabajo grupal que los estudiantes puedan realizar durante la clase para aplicar el tema {tema}. Incluir instrucciones claras y objetivos del trabajo grupal. Objetivos: {objetivo_general} y {objetivo_durante}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar trabajo grupal: {e}")

def generar_herramientas_externas(tema, objetivo_general, objetivo_durante):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Listar tres herramientas o recursos externos en HTML que los estudiantes puedan utilizar durante la clase para explorar más sobre el tema {tema}. Incluir una breve descripción y enlaces a los recursos. Objetivos: {objetivo_general} y {objetivo_durante}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar herramientas externas: {e}")

def generar_resumen_clase(tema, objetivo_general, objetivo_despues):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Proveer un resumen en HTML de 100 palabras que recapitule los puntos principales cubiertos durante la clase sobre {tema}. El resumen debe destacar los conceptos clave y su aplicación. Objetivos: {objetivo_general} y {objetivo_despues}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar resumen de clase: {e}")

def generar_cuestionario_despues(tema, objetivo_general, objetivo_despues):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Generar un cuestionario de evaluación en HTML con cinco preguntas de opción múltiple para ser completado después de la clase sobre {tema}. Cada pregunta debe tener cuatro opciones de respuesta, incluyendo una correcta. Objetivos: {objetivo_general} y {objetivo_despues}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar cuestionario después de clase: {e}")

def generar_trabajo_despues_clase(tema, objetivo_general, objetivo_despues):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Describir una tarea o proyecto en HTML que los estudiantes deben completar después de la clase para reforzar su comprensión del tema {tema}. Incluir los objetivos de la tarea y los criterios de evaluación. Objetivos: {objetivo_general} y {objetivo_despues}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar trabajo para después de clase: {e}")

def generar_recomendacion_libros(tema, objetivo_general, objetivo_despues):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Proveer una lista en HTML de tres libros recomendados para profundizar en el tema {tema}. Incluir el título del libro, el autor y una breve descripción de su contenido. Objetivos: {objetivo_general} y {objetivo_despues}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar recomendación de libros: {e}")

def generar_recomendaciones(tema, objetivo_general, objetivo_despues):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Ofrecer tres recomendaciones en HTML para los estudiantes sobre cómo pueden continuar aprendiendo y aplicando el tema {tema} después de la clase. Incluir enlaces a recursos adicionales si es relevante. Objetivos: {objetivo_general} y {objetivo_despues}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar recomendaciones: {e}")

def generar_ejercicios_practicar(tema, objetivo_general, objetivo_despues):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Crear tres ejercicios adicionales en HTML que los estudiantes puedan hacer después de la clase para practicar el tema {tema}. Cada ejercicio debe incluir una descripción y los requisitos. Objetivos: {objetivo_general} y {objetivo_despues}."}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error al generar ejercicios para practicar: {e}")
