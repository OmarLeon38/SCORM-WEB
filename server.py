import os
import tempfile
import logging
from flask import Flask, request, jsonify, render_template, url_for, redirect, session, send_file
from flask_cors import CORS
from flask_session import Session
import scorm_generator
import openai_generator
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

scorm_gen = scorm_generator.ScormGenerator()

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/contenido_generado')
def contenido_generado():
    if 'contenido_generado' in session:
        contenido_generado = session['contenido_generado']
        return render_template('contenido_generado.html', contenido_generado=contenido_generado)
    else:
        return redirect(url_for('index'))

@app.route('/generar_contenido', methods=['POST'])
def generar_contenido():
    data = request.json
    logging.debug(f"Datos recibidos: {data}")
    tema = data['tema']
    objetivo_general = data['objetivo_general']
    objetivo_antes = data['objetivo_antes']
    objetivo_durante = data['objetivo_durante']
    objetivo_despues = data['objetivo_despues']
    seleccion = data['seleccion']
    
    session.pop('contenido_generado', None)
    session.pop('seleccion', None)
    
    contenido_generado = {}
    try:
        if "motivacion" in seleccion["antes"]:
            contenido_generado["motivacion"] = openai_generator.generar_motivacion(tema, objetivo_general, objetivo_antes)
        if "objetivos_clase" in seleccion["antes"]:
            contenido_generado["objetivos_clase"] = openai_generator.generar_objetivos_clase(tema, objetivo_general, objetivo_antes)
        if "preguntas_motivacion" in seleccion["antes"]:
            contenido_generado["preguntas_motivacion"] = openai_generator.generar_preguntas_motivacion(tema, objetivo_general, objetivo_antes)
        if "introduccion_tema" in seleccion["antes"]:
            contenido_generado["introduccion_tema"] = openai_generator.generar_informacion(tema, objetivo_general, objetivo_antes)
        if "video_introductorio" in seleccion["antes"]:
            contenido_generado["video_introductorio"] = openai_generator.generar_video_youtube(tema)
        if "cuestionario_conocimientos_previos" in seleccion["antes"]:
            contenido_generado["cuestionario_conocimientos_previos"] = openai_generator.generar_cuestionario_conocimientos_previos(tema, objetivo_general, objetivo_antes)
        if "conceptos_basicos" in seleccion["antes"]:
            contenido_generado["conceptos_basicos"] = openai_generator.generar_conceptos_basicos(tema, objetivo_general, objetivo_antes)
        if "contenido_clase" in seleccion["durante"]:
            contenido_generado["contenido_clase"] = openai_generator.generar_contenido_clase(tema, objetivo_general, objetivo_durante)
        if "ejemplos_casos_reales" in seleccion["durante"]:
            contenido_generado["ejemplos_casos_reales"] = openai_generator.generar_ejemplos_casos_reales(tema, objetivo_general, objetivo_durante)
        if "tarea_individual" in seleccion["durante"]:
            contenido_generado["tarea_individual"] = openai_generator.generar_tarea_individual(tema, objetivo_general, objetivo_durante)
        if "tarea_grupal" in seleccion["durante"]:
            contenido_generado["tarea_grupal"] = openai_generator.generar_tarea_grupal(tema, objetivo_general, objetivo_durante)
        if "herramientas_externas" in seleccion["durante"]:
            contenido_generado["herramientas_externas"] = openai_generator.generar_herramientas_externas(tema, objetivo_general, objetivo_durante)
        if "ejercicios_programacion" in seleccion["durante"]:
            contenido_generado["ejercicios_programacion"] = openai_generator.generar_ejercicios_programacion(tema, objetivo_general, objetivo_durante)
        if "ejercicios_completar_codigo" in seleccion["durante"]:
            contenido_generado["ejercicios_completar_codigo"] = openai_generator.generar_ejercicios_completar_codigo(tema, objetivo_general, objetivo_durante)
        if "ejercicios_corregir_codigo" in seleccion["durante"]:
            contenido_generado["ejercicios_corregir_codigo"] = openai_generator.generar_ejercicios_corregir_codigo(tema, objetivo_general, objetivo_durante)
        if "proyecto_clase" in seleccion["durante"]:
            contenido_generado["proyecto_clase"] = openai_generator.generar_proyecto_clase(tema, objetivo_general, objetivo_durante)
        if "cuestionario_final" in seleccion["despues"]:
            contenido_generado["cuestionario_final"] = openai_generator.generar_cuestionario_final(tema, objetivo_general, objetivo_despues)
        if "ejercicios_practicar" in seleccion["despues"]:
            contenido_generado["ejercicios_practicar"] = openai_generator.generar_ejercicios_practicar(tema, objetivo_general, objetivo_despues)
        if "tarea_despues_clase" in seleccion["despues"]:
            contenido_generado["tarea_despues_clase"] = openai_generator.generar_tarea_despues_clase(tema, objetivo_general, objetivo_despues)
        if "resumen_final" in seleccion["despues"]:
            contenido_generado["resumen_final"] = openai_generator.generar_resumen_clase(tema, objetivo_general, objetivo_despues)
        if "recomendacion_libros" in seleccion["despues"]:
            contenido_generado["recomendacion_libros"] = openai_generator.generar_recomendacion_libros(tema, objetivo_general, objetivo_despues)
        if "aplicacion_problemas_reales" in seleccion["despues"]:
            contenido_generado["aplicacion_problemas_reales"] = openai_generator.generar_aplicacion_problemas_reales(tema, objetivo_general, objetivo_despues)

        logging.debug("Contenido generado: %s", contenido_generado)
        
        session['contenido_generado'] = contenido_generado
        session['seleccion'] = seleccion
        response = {'redirect_url': url_for('contenido_generado')}
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/confirmar', methods=['POST'])
def confirmar():
    if 'contenido_generado' in session and 'seleccion' in session:
        contenido_generado = session['contenido_generado']
        seleccion = session['seleccion']
        try:
            ruta_zip = scorm_gen.generar_paquete_scorm(contenido_generado, seleccion)
            filename = os.path.basename(ruta_zip)
            return jsonify({'status': 'Contenido confirmado y paquete SCORM generado', 'ruta': url_for('descargar', filename=filename)})
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            return jsonify({'status': 'Error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'Error', 'message': 'Contenido o selección no encontrados en la sesión'}), 400

@app.route('/descargar/<filename>', methods=['GET'])
def descargar(filename):
    try:
        return send_file(os.path.join(tempfile.gettempdir(), filename), as_attachment=True)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return str(e)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000, connection_limit=100, connection_timeout=600)