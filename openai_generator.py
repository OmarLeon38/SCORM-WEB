import aiohttp
import os
from dotenv import load_dotenv
import logging

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_timeout = 180  # tiempo de espera en segundos

async def fetch_openai(api_url, payload):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer " + openai_api_key,
            "Content-Type": "application/json"
        }
        async with session.post(api_url, json=payload, headers=headers, timeout=openai_timeout) as response:
            response.raise_for_status()
            return await response.json()

async def generar_motivacion(tema, objetivo_general, objetivo_antes):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Escribir un párrafo en HTML motivacional sobre la importancia de estudiar {tema}. Objetivos: {objetivo_general}, {objetivo_antes}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar motivación: {e}")
        raise RuntimeError(f"Error al generar motivación: {e}")

async def generar_objetivos_clase(tema, objetivo_general, objetivo_antes):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Generar una lista en HTML de objetivos de aprendizaje claros y específicos para una clase sobre {tema}. Objetivos: {objetivo_general}, {objetivo_antes}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar objetivos de la clase: {e}")
        raise RuntimeError(f"Error al generar objetivos de la clase: {e}")

async def generar_preguntas_motivacion(tema, objetivo_general, objetivo_antes):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Generar tres preguntas en HTML de motivación sobre {tema}. Objetivos: {objetivo_general}, {objetivo_antes}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar preguntas de motivación: {e}")
        raise RuntimeError(f"Error al generar preguntas de motivación: {e}")

async def generar_informacion(tema, objetivo_general, objetivo_antes):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Escribir un resumen en HTML sobre {tema}. Objetivos: {objetivo_general}, {objetivo_antes}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar información: {e}")
        raise RuntimeError(f"Error al generar información: {e}")

async def generar_video_youtube(tema):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Buscar un enlace de YouTube sobre un video educativo relevante a {tema}. Solo generar el enlace en HTML."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar enlace de video: {e}")
        raise RuntimeError(f"Error al generar enlace de video: {e}")

async def generar_cuestionario_conocimientos_previos(tema, objetivo_general, objetivo_antes):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": f"Generar un cuestionario en JSON con cinco preguntas de opción múltiple sobre {tema} para evaluar conocimientos previos. Las preguntas deben tener el siguiente formato: {{ 'pregunta': 'Pregunta', 'opciones': ['opcion1', 'opcion2', 'opcion3', 'opcion4'], 'respuesta': 'respuesta_correcta' }}. Objetivos: {objetivo_general}, {objetivo_antes}."
                }
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar cuestionario de conocimientos previos: {e}")
        raise RuntimeError(f"Error al generar cuestionario de conocimientos previos: {e}")

async def generar_conceptos_basicos(tema, objetivo_general, objetivo_antes):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Escribir un documento en HTML que explique los conceptos básicos sobre {tema}. Objetivos: {objetivo_general}, {objetivo_antes}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar conceptos básicos: {e}")
        raise RuntimeError(f"Error al generar conceptos básicos: {e}")

async def generar_contenido_clase(tema, objetivo_general, objetivo_durante):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Proveer un esquema en HTML detallado del contenido que se debe cubrir durante una clase sobre {tema}. Objetivos: {objetivo_general}, {objetivo_durante}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar contenido de clase: {e}")
        raise RuntimeError(f"Error al generar contenido de clase: {e}")

async def generar_ejemplos_casos_reales(tema, objetivo_general, objetivo_durante):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Proveer dos ejemplos en HTML de la vida real que demuestren la aplicación práctica de {tema}. Objetivos: {objetivo_general}, {objetivo_durante}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar ejemplos de casos reales: {e}")
        raise RuntimeError(f"Error al generar ejemplos de casos reales: {e}")

async def generar_tarea_individual(tema, objetivo_general, objetivo_durante):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Describir una tarea individual en HTML que los estudiantes pueden realizar durante la clase sobre {tema}. Objetivos: {objetivo_general}, {objetivo_durante}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar tarea individual: {e}")
        raise RuntimeError(f"Error al generar tarea individual: {e}")

async def generar_tarea_grupal(tema, objetivo_general, objetivo_durante):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Describir una tarea grupal en HTML que los estudiantes pueden realizar durante la clase sobre {tema}. Objetivos: {objetivo_general}, {objetivo_durante}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar tarea grupal: {e}")
        raise RuntimeError(f"Error al generar tarea grupal: {e}")

async def generar_herramientas_externas(tema, objetivo_general, objetivo_durante):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Listar tres herramientas o recursos externos en HTML que los estudiantes pueden utilizar durante la clase para explorar más sobre {tema}. Objetivos: {objetivo_general}, {objetivo_durante}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar herramientas externas: {e}")
        raise RuntimeError(f"Error al generar herramientas externas: {e}")

async def generar_ejercicios_programacion(tema, objetivo_general, objetivo_durante):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Crear tres ejercicios de programación en HTML que los estudiantes puedan realizar durante la clase sobre {tema}. Objetivos: {objetivo_general}, {objetivo_durante}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar ejercicios de programación: {e}")
        raise RuntimeError(f"Error al generar ejercicios de programación: {e}")

async def generar_ejercicios_completar_codigo(tema, objetivo_general, objetivo_durante):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Crear ejercicios en HTML donde los estudiantes deben completar el código relacionado con {tema}. Objetivos: {objetivo_general}, {objetivo_durante}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar ejercicios para completar código: {e}")
        raise RuntimeError(f"Error al generar ejercicios para completar código: {e}")

async def generar_ejercicios_corregir_codigo(tema, objetivo_general, objetivo_durante):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Crear ejercicios en HTML donde los estudiantes deben corregir errores en el código relacionado con {tema}. Objetivos: {objetivo_general}, {objetivo_durante}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar ejercicios para corregir código: {e}")
        raise RuntimeError(f"Error al generar ejercicios para corregir código: {e}")

async def generar_proyecto_clase(tema, objetivo_general, objetivo_durante):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Describir un proyecto en HTML que los estudiantes deben realizar durante la clase sobre {tema}. Objetivos: {objetivo_general}, {objetivo_durante}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar proyecto de clase: {e}")
        raise RuntimeError(f"Error al generar proyecto de clase: {e}")

async def generar_cuestionario_final(tema, objetivo_general, objetivo_despues):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": f"Generar un cuestionario en JSON con cinco preguntas de opción múltiple sobre {tema} para evaluar al final de la clase. Las preguntas deben tener el siguiente formato: {{ 'pregunta': 'Pregunta', 'opciones': ['opcion1', 'opcion2', 'opcion3', 'opcion4'], 'respuesta': 'respuesta_correcta' }}. Objetivos: {objetivo_general}, {objetivo_despues}."
                }
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar cuestionario final: {e}")
        raise RuntimeError(f"Error al generar cuestionario final: {e}")

async def generar_ejercicios_practicar(tema, objetivo_general, objetivo_despues):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Crear tres ejercicios adicionales en HTML para practicar {tema} después de la clase. Objetivos: {objetivo_general}, {objetivo_despues}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar ejercicios para practicar: {e}")
        raise RuntimeError(f"Error al generar ejercicios para practicar: {e}")

async def generar_resumen_clase(tema, objetivo_general, objetivo_despues):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Proveer un resumen en HTML que recapitule los puntos principales sobre {tema}. Objetivos: {objetivo_general}, {objetivo_despues}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar resumen de clase: {e}")
        raise RuntimeError(f"Error al generar resumen de clase: {e}")

async def generar_tarea_despues_clase(tema, objetivo_general, objetivo_despues):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Describir una tarea en HTML que los estudiantes deben completar después de la clase sobre {tema}. Objetivos: {objetivo_general}, {objetivo_despues}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar tarea para después de clase: {e}")
        raise RuntimeError(f"Error al generar tarea para después de clase: {e}")

async def generar_recomendacion_libros(tema, objetivo_general, objetivo_despues):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Proveer una lista en HTML de tres libros recomendados para profundizar en {tema}. Objetivos: {objetivo_general}, {objetivo_despues}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar recomendación de libros: {e}")
        raise RuntimeError(f"Error al generar recomendación de libros: {e}")

async def generar_aplicacion_problemas_reales(tema, objetivo_general, objetivo_despues):
    try:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Crear actividades en HTML que muestren cómo aplicar {tema} a problemas del mundo real. Objetivos: {objetivo_general}, {objetivo_despues}."}
            ]
        }
        response = await fetch_openai("https://api.openai.com/v1/chat/completions", payload)
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error al generar aplicación en problemas reales: {e}")
        raise RuntimeError(f"Error al generar aplicación en problemas reales: {e}")