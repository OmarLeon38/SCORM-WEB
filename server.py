from quart import Quart, request, jsonify, render_template, url_for, redirect, session
from quart_cors import cors
from quart_session import Session
import asyncio
import scorm_generator
import openai_generator
import logging

app = Quart(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

# Configuración de Quart-Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

scorm_gen = scorm_generator.ScormGenerator()

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/contenido_generado')
async def contenido_generado():
    if 'contenido_generado' in session:
        contenido_generado = session['contenido_generado']
        return await render_template('contenido_generado.html', contenido_generado=contenido_generado)
    else:
        return redirect(url_for('index'))

async def generar_contenido_seccion(tema, objetivo_general, objetivo, seleccion, seccion):
    contenido_generado = {}
    try:
        if seccion == "antes":
            if "motivacion" in seleccion:
                contenido_generado["motivacion"] = await openai_generator.generar_motivacion(tema, objetivo_general, objetivo)
            if "objetivos_clase" in seleccion:
                contenido_generado["objetivos_clase"] = await openai_generator.generar_objetivos_clase(tema, objetivo_general, objetivo)
            if "preguntas_motivacion" in seleccion:
                contenido_generado["preguntas_motivacion"] = await openai_generator.generar_preguntas_motivacion(tema, objetivo_general, objetivo)
            if "introduccion_tema" in seleccion:
                contenido_generado["introduccion_tema"] = await openai_generator.generar_informacion(tema, objetivo_general, objetivo)
            if "video_introductorio" in seleccion:
                contenido_generado["video_introductorio"] = await openai_generator.generar_video_youtube(tema)
            if "cuestionario_conocimientos_previos" in seleccion:
                contenido_generado["cuestionario_conocimientos_previos"] = await openai_generator.generar_cuestionario_conocimientos_previos(tema, objetivo_general, objetivo)
            if "conceptos_basicos" in seleccion:
                contenido_generado["conceptos_basicos"] = await openai_generator.generar_conceptos_basicos(tema, objetivo_general, objetivo)
        elif seccion == "durante":
            if "contenido_clase" in seleccion:
                contenido_generado["contenido_clase"] = await openai_generator.generar_contenido_clase(tema, objetivo_general, objetivo)
            if "ejemplos_casos_reales" in seleccion:
                contenido_generado["ejemplos_casos_reales"] = await openai_generator.generar_ejemplos_casos_reales(tema, objetivo_general, objetivo)
            if "tarea_individual" in seleccion:
                contenido_generado["tarea_individual"] = await openai_generator.generar_tarea_individual(tema, objetivo_general, objetivo)
            if "tarea_grupal" in seleccion:
                contenido_generado["tarea_grupal"] = await openai_generator.generar_tarea_grupal(tema, objetivo_general, objetivo)
            if "herramientas_externas" in seleccion:
                contenido_generado["herramientas_externas"] = await openai_generator.generar_herramientas_externas(tema, objetivo_general, objetivo)
            if "ejercicios_programacion" in seleccion:
                contenido_generado["ejercicios_programacion"] = await openai_generator.generar_ejercicios_programacion(tema, objetivo_general, objetivo)
            if "ejercicios_completar_codigo" in seleccion:
                contenido_generado["ejercicios_completar_codigo"] = await openai_generator.generar_ejercicios_completar_codigo(tema, objetivo_general, objetivo)
            if "ejercicios_corregir_codigo" in seleccion:
                contenido_generado["ejercicios_corregir_codigo"] = await openai_generator.generar_ejercicios_corregir_codigo(tema, objetivo_general, objetivo)
            if "proyecto_clase" in seleccion:
                contenido_generado["proyecto_clase"] = await openai_generator.generar_proyecto_clase(tema, objetivo_general, objetivo)
        elif seccion == "despues":
            if "cuestionario_final" in seleccion:
                contenido_generado["cuestionario_final"] = await openai_generator.generar_cuestionario_final(tema, objetivo_general, objetivo)
            if "ejercicios_practicar" in seleccion:
                contenido_generado["ejercicios_practicar"] = await openai_generator.generar_ejercicios_practicar(tema, objetivo_general, objetivo)
            if "resumen_final" in seleccion:
                contenido_generado["resumen_final"] = await openai_generator.generar_resumen_clase(tema, objetivo_general, objetivo)
            if "tarea_despues_clase" in seleccion:
                contenido_generado["tarea_despues_clase"] = await openai_generator.generar_tarea_despues_clase(tema, objetivo_general, objetivo)
            if "recomendacion_libros" in seleccion:
                contenido_generado["recomendacion_libros"] = await openai_generator.generar_recomendacion_libros(tema, objetivo_general, objetivo)
            if "aplicacion_problemas_reales" in seleccion:
                contenido_generado["aplicacion_problemas_reales"] = await openai_generator.generar_aplicacion_problemas_reales(tema, objetivo_general, objetivo)
    except Exception as e:
        logging.error(f"Error al generar contenido para la sección {seccion}: {str(e)}")
        return None
    return contenido_generado

@app.route('/generar_contenido', methods=['POST'])
async def generar_contenido():
    data = await request.json
    tema = data['tema']
    objetivo_general = data['objetivo_general']
    objetivo_antes = data['objetivo_antes']
    objetivo_durante = data['objetivo_durante']
    objetivo_despues = data['objetivo_despues']
    seleccion = data['seleccion']
    
    # Limpiar la sesión antes de almacenar el nuevo contenido
    session.pop('contenido_generado', None)
    session.pop('seleccion', None)
    
    contenido_generado = {}
    print(f"Datos recibidos: {data}")
    try:
        tareas = []
        if seleccion["antes"]:
            tareas.append(generar_contenido_seccion(tema, objetivo_general, objetivo_antes, seleccion["antes"], "antes"))
        if seleccion["durante"]:
            tareas.append(generar_contenido_seccion(tema, objetivo_general, objetivo_durante, seleccion["durante"], "durante"))
        if seleccion["despues"]:
            tareas.append(generar_contenido_seccion(tema, objetivo_general, objetivo_despues, seleccion["despues"], "despues"))
        
        resultados = await asyncio.gather(*tareas)
        for resultado in resultados:
            if resultado:
                contenido_generado.update(resultado)
        
        # Imprimir el contenido generado para depuración
        print("Contenido generado:", contenido_generado)
        
        session['contenido_generado'] = contenido_generado
        session['seleccion'] = seleccion  # Guardar la selección en la sesión
        return jsonify({'redirect_url': url_for('contenido_generado')})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/confirmar', methods=['POST'])
async def confirmar():
    if 'contenido_generado' in session and 'seleccion' in session:
        contenido_generado = session['contenido_generado']
        seleccion = session['seleccion']
        try:
            ruta_zip = await scorm_gen.generar_paquete_scorm(contenido_generado, seleccion)
            return jsonify({'status': 'Contenido confirmado y paquete SCORM generado', 'ruta': ruta_zip})
        except Exception as e:
            return jsonify({'status': 'Error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'Error', 'message': 'Contenido o selección no encontrados en la sesión'}), 400

if __name__ == "__main__":
    app.run(port=5000)