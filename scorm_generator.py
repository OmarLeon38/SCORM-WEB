import os
import shutil
import zipfile
import tempfile

class ScormGenerator:
    def __init__(self):
        self.scorm_dir = self.create_temp_dir()
        self.seccion_carpeta_map = {
            'motivacion': 'antes_clase',
            'objetivos_clase': 'antes_clase',
            'preguntas_motivacion': 'antes_clase',
            'introduccion_tema': 'antes_clase',
            'video_introductorio': 'antes_clase',
            'cuestionario_conocimientos_previos': 'antes_clase/cuestionario_conocimientos_previos',
            'conceptos_basicos': 'antes_clase',
            'contenido_clase': 'durante_clase',
            'ejemplos_casos_reales': 'durante_clase',
            'tarea_individual': 'durante_clase',
            'tarea_grupal': 'durante_clase',
            'herramientas_externas': 'durante_clase',
            'ejercicios_programacion': 'durante_clase',
            'ejercicios_completar_codigo': 'durante_clase',
            'ejercicios_corregir_codigo': 'durante_clase',
            'proyecto_clase': 'durante_clase',
            'cuestionario_final': 'despues_clase/cuestionario_final',
            'ejercicios_practicar': 'despues_clase',
            'resumen_final': 'despues_clase',
            'tarea_despues_clase': 'despues_clase',
            'recomendacion_libros': 'despues_clase',
            'aplicacion_problemas_reales': 'despues_clase'
        }

    def create_temp_dir(self):
        temp_dir = tempfile.mkdtemp()
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        return temp_dir

    def limpiar_archivos_antiguos(self):
        if os.path.exists(self.scorm_dir):
            shutil.rmtree(self.scorm_dir)
        self.scorm_dir = self.create_temp_dir()

    def copiar_archivos_estaticos_y_config(self, config):
        for section, content in config.items():
            carpeta_plantillas = self.seccion_carpeta_map.get(section, '')
            directorio_destino = os.path.join(self.scorm_dir, carpeta_plantillas)
            os.makedirs(directorio_destino, exist_ok=True)
            
            if section in ['cuestionario_conocimientos_previos', 'cuestionario_final']:
                archivo_html_origen = os.path.join('plantillas', carpeta_plantillas, 'index.html')
                archivo_html_destino = os.path.join(directorio_destino, 'index.html')
                if os.path.exists(archivo_html_origen):
                    contenido_actualizado = self.actualizar_html_con_preguntas(archivo_html_origen, content)
                    with open(archivo_html_destino, 'w', encoding='utf-8') as file:
                        file.write(contenido_actualizado)
                shutil.copy(os.path.join('plantillas', carpeta_plantillas, 'styles.css'), os.path.join(directorio_destino, 'styles.css'))
            else:
                archivo_html_origen = os.path.join('plantillas', carpeta_plantillas, f"{section}.html")
                archivo_html_destino = os.path.join(directorio_destino, f"{section}.html")
                if os.path.exists(archivo_html_origen):
                    contenido_actualizado = self.actualizar_html(archivo_html_origen, {section: content})
                    with open(archivo_html_destino, 'w', encoding='utf-8') as file:
                        file.write(contenido_actualizado)
                
                nombre_archivo_css = f"estilos_{carpeta_plantillas.split('/')[0]}.css"
                archivo_css_origen = os.path.join('plantillas', carpeta_plantillas.split('/')[0], nombre_archivo_css)
                archivo_css_destino = os.path.join(directorio_destino, nombre_archivo_css)
                if os.path.exists(archivo_css_origen):
                    shutil.copy(archivo_css_origen, archivo_css_destino)
                    
    def actualizar_html(self, html_path, placeholders):
        if not os.path.exists(html_path):
            raise FileNotFoundError(f"El archivo no existe: {html_path}")
        with open(html_path, 'r', encoding='utf-8') as file:
            content = file.read()
        for key, value in placeholders.items():
            placeholder = f"{{{{ {key} }}}}"
            content = content.replace(placeholder, value)
        return content
    
    def actualizar_html_con_preguntas(self, html_path, preguntas_json):
        if not os.path.exists(html_path):
            raise FileNotFoundError(f"El archivo no existe: {html_path}")
        with open(html_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        preguntas_js = f"const bd_juego = {preguntas_json};"
        content = content.replace("{{ preguntas }}", preguntas_js)
        return content
    
    def generar_imsmanifest(self, seleccion):
        # Generar el manifiesto SCORM basado en la selección del usuario
        items_antes = []
        items_durante = []
        items_despues = []
        resources = []
        def agregar_recurso(section, carpeta):
            if section in seleccion["antes"]:
                items_antes.append(f"""
                    <item identifier="ITEM_{section.upper()}" identifierref="REF_{section.upper()}">
                        <title>{section.replace('_', ' ').capitalize()}</title>
                    </item>
                """)
            elif section in seleccion["durante"]:
                items_durante.append(f"""
                    <item identifier="ITEM_{section.upper()}" identifierref="REF_{section.upper()}">
                        <title>{section.replace('_', ' ').capitalize()}</title>
                    </item>
                """)
            elif section in seleccion["despues"]:
                items_despues.append(f"""
                    <item identifier="ITEM_{section.upper()}" identifierref="REF_{section.upper()}">
                        <title>{section.replace('_', ' ').capitalize()}</title>
                    </item>
                """)
            
            if section in ['cuestionario_conocimientos_previos', 'cuestionario_final']:
                resources.append(f"""
                    <resource identifier="REF_{section.upper()}" type="webcontent" adlcp:scormtype="sco" href="{carpeta}/index.html">
                        <file href="{carpeta}/index.html"/>
                        <file href="{carpeta}/config.json"/>
                        <file href="{carpeta}/script.js"/>
                        <file href="{carpeta}/styles.css"/>
                    </resource>
                """)
            else:
                resources.append(f"""
                    <resource identifier="REF_{section.upper()}" type="webcontent" adlcp:scormtype="sco" href="{carpeta}/{section}.html">
                        <file href="{carpeta}/{section}.html"/>
                        <file href="{carpeta}/estilos_{carpeta.split('/')[0]}.css"/>
                    </resource>
                """)
        for section in seleccion["antes"]:
            agregar_recurso(section, self.seccion_carpeta_map[section])
        for section in seleccion["durante"]:
            agregar_recurso(section, self.seccion_carpeta_map[section])
        for section in seleccion["despues"]:
            agregar_recurso(section, self.seccion_carpeta_map[section])
        contenido_imsmanifest = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
        xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
                            http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd"
        identifier="MANIFEST_ID"
        version="1.0">
    <metadata>
        <schema>ADL SCORM</schema>
        <schemaversion>1.2</schemaversion>
    </metadata>
    <organizations default="ORGANIZACION_SCORM">
        <organization identifier="ORGANIZACION_SCORM">
            <title>Curso de Estructura de Datos</title>
            <item identifier="ANTES_CLASE">
                <title>Antes de clase</title>
                {"".join(items_antes)}
            </item>
            <item identifier="DURANTE_CLASE">
                <title>Durante la clase</title>
                {"".join(items_durante)}
            </item>
            <item identifier="DESPUES_CLASE">
                <title>Después de clase</title>
                {"".join(items_despues)}
            </item>
        </organization>
    </organizations>
    <resources>
        {"".join(resources)}
    </resources>
</manifest>
        """
        # Escribir el manifiesto en un archivo `imsmanifest.xml`
        manifest_path = os.path.join(self.scorm_dir, "imsmanifest.xml")
        with open(manifest_path, "w", encoding="utf-8") as file:
            file.write(contenido_imsmanifest)

    def empaquetar_scorm(self):
        # Empaqueta todos los archivos en un ZIP para el paquete SCORM
        zip_path = os.path.join(tempfile.gettempdir(), 'paquete_scorm.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(self.scorm_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.scorm_dir))
        print("Empaquetado completado. Archivo ZIP guardado en:", zip_path)
        return zip_path

    def generar_paquete_scorm(self, config, seleccion):
        # Limpiar cualquier archivo SCORM previo antes de generar uno nuevo
        self.limpiar_archivos_antiguos()
        # Copia las plantillas, actualiza con los marcadores y empaqueta
        self.copiar_archivos_estaticos_y_config(config)
        self.generar_imsmanifest(seleccion)
        return self.empaquetar_scorm()