from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import scorm_generator
import openai_generator

app = Flask(__name__)
CORS(app)
scorm_gen = scorm_generator.ScormGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_contenido', methods=['POST'])
def generar_contenido():
    data = request.json
    tema = data['tema']
    objetivo_general = data['objetivo_general']
    objetivo_antes = data['objetivo_antes']
    objetivo_durante = data['objetivo_durante']
    objetivo_despues = data['objetivo_despues']
    seleccion = data['seleccion']
    
    contenido_generado = {}
    try:
        if "resumen_tema" in seleccion["antes"]:
            contenido_generado["resumen_tema"] = openai_generator.generar_informacion(tema, objetivo_general, objetivo_antes)
        if "video_introductorio" in seleccion["antes"]:
            contenido_generado["video_introductorio"] = openai_generator.generar_video_youtube(tema)
        if "objetivos_clase" in seleccion["antes"]:
            contenido_generado["objetivos_clase"] = openai_generator.generar_objetivos_clase(tema, objetivo_general, objetivo_antes)
        if "preguntas_motivacion" in seleccion["antes"]:
            contenido_generado["preguntas_motivacion"] = openai_generator.generar_preguntas_motivacion(tema, objetivo_general, objetivo_antes)
        if "cuestionario" in seleccion["antes"]:
            contenido_generado["cuestionario"] = openai_generator.generar_cuestionario(tema, objetivo_general, objetivo_antes)
        if "motivacion" in seleccion["antes"]:
            contenido_generado["motivacion"] = openai_generator.generar_motivacion(tema, objetivo_general, objetivo_antes)
        if "contenido_clase" in seleccion["durante"]:
            contenido_generado["contenido_clase"] = openai_generator.generar_contenido_clase(tema, objetivo_general, objetivo_durante)
        if "ejercicios_programacion" in seleccion["durante"]:
            contenido_generado["ejercicios_programacion"] = openai_generator.generar_ejercicios_programacion(tema, objetivo_general, objetivo_durante)
        if "ejemplos_casos_reales" in seleccion["durante"]:
            contenido_generado["ejemplos_casos_reales"] = openai_generator.generar_ejemplos_casos_reales(tema, objetivo_general, objetivo_durante)
        if "juego_preguntas" in seleccion["durante"]:
            contenido_generado["juego_preguntas"] = openai_generator.generar_json_pasapalabra(tema, objetivo_general, objetivo_durante)
        if "trabajo_grupal" in seleccion["durante"]:
            contenido_generado["trabajo_grupal"] = openai_generator.generar_trabajo_grupal(tema, objetivo_general, objetivo_durante)
        if "herramientas_externas" in seleccion["durante"]:
            contenido_generado["herramientas_externas"] = openai_generator.generar_herramientas_externas(tema, objetivo_general, objetivo_durante)
        if "resumen_clase" in seleccion["despues"]:
            contenido_generado["resumen_clase"] = openai_generator.generar_resumen_clase(tema, objetivo_general, objetivo_despues)
        if "cuestionario_despues" in seleccion["despues"]:
            contenido_generado["cuestionario_despues"] = openai_generator.generar_cuestionario_despues(tema, objetivo_general, objetivo_despues)
        if "trabajo_despues_clase" in seleccion["despues"]:
            contenido_generado["trabajo_despues_clase"] = openai_generator.generar_trabajo_despues_clase(tema, objetivo_general, objetivo_despues)
        if "recomendacion_libros" in seleccion["despues"]:
            contenido_generado["recomendacion_libros"] = openai_generator.generar_recomendacion_libros(tema, objetivo_general, objetivo_despues)
        if "recomendaciones" in seleccion["despues"]:
            contenido_generado["recomendaciones"] = openai_generator.generar_recomendaciones(tema, objetivo_general, objetivo_despues)
        if "ejercicios_practicar" in seleccion["despues"]:
            contenido_generado["ejercicios_practicar"] = openai_generator.generar_ejercicios_practicar(tema, objetivo_general, objetivo_despues)
        
        return jsonify({'contenido': contenido_generado})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/confirmar', methods=['POST'])
def confirmar():
    data = request.json
    contenido_generado = data['contenido']
    seleccion = data['seleccion']
    try:
        ruta_zip = scorm_gen.generar_paquete_scorm(contenido_generado, seleccion)
        return jsonify({'status': 'Contenido confirmado y paquete SCORM generado', 'ruta': ruta_zip})
    except Exception as e:
        return jsonify({'status': 'Error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)