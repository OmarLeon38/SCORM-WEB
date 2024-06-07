import os
import shutil
import zipfile

class ScormGenerator:
    def __init__(self, scorm_dir='C:/paquete_scorm'):
        self.scorm_dir = scorm_dir
        os.makedirs(self.scorm_dir, exist_ok=True)
        self.seccion_carpeta_map = {
            'resumen_tema': 'antes_clase',
            'video_introductorio': 'antes_clase',
            'objetivos_clase': 'antes_clase',
            'preguntas_motivacion': 'antes_clase',
            'cuestionario': 'antes_clase',
            'motivacion': 'antes_clase',
            'contenido_clase': 'durante_clase',
            'ejercicios_programacion': 'durante_clase',
            'ejemplos_casos_reales': 'durante_clase',
            'juego_preguntas': 'durante_clase',
            'trabajo_grupal': 'durante_clase',
            'herramientas_externas': 'durante_clase',
            'resumen_clase': 'despues_clase',
            'cuestionario_despues': 'despues_clase',
            'trabajo_despues_clase': 'despues_clase',
            'recomendacion_libros': 'despues_clase',
            'recomendaciones': 'despues_clase',
            'ejercicios_practicar': 'despues_clase'
        }

    def copiar_archivos_estaticos_y_config(self, config):
        for section, content in config.items():
            carpeta_plantillas = self.seccion_carpeta_map[section]
            directorio_destino = os.path.join(self.scorm_dir, carpeta_plantillas)
            os.makedirs(directorio_destino, exist_ok=True)
            
            archivo_html_origen = os.path.join('plantillas', carpeta_plantillas, f"{section}.html")
            archivo_html_destino = os.path.join(directorio_destino, f"{section}.html")
            if os.path.exists(archivo_html_origen):
                contenido_actualizado = self.actualizar_html(archivo_html_origen, {section: content})
                with open(archivo_html_destino, 'w', encoding='utf-8') as file:
                    file.write(contenido_actualizado)
            
            nombre_archivo_css = f"estilos_{carpeta_plantillas.split('/')[-1]}.css"
            archivo_css_origen = os.path.join('plantillas', carpeta_plantillas, nombre_archivo_css)
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

    def generar_imsmanifest(self, seleccion):
        items = []
        resources = []

        def agregar_recurso(section, carpeta):
            items.append(f"""
                <item identifier="ITEM_{section.upper()}" identifierref="REF_{section.upper()}">
                    <title>{section.replace('_', ' ').capitalize()}</title>
                </item>
            """)
            resources.append(f"""
                <resource identifier="REF_{section.upper()}" type="webcontent" adlcp:scormtype="sco" href="{carpeta}/{section}.html">
                    <file href="{carpeta}/{section}.html"/>
                    <file href="{carpeta}/estilos_{carpeta}.css"/>
                </resource>
            """)

        for section in seleccion["antes"]:
            agregar_recurso(section, 'antes_clase')

        for section in seleccion["durante"]:
            agregar_recurso(section, 'durante_clase')

        for section in seleccion["despues"]:
            agregar_recurso(section, 'despues_clase')

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
            {"".join(items)}
        </organization>
    </organizations>
    <resources>
        {"".join(resources)}
    </resources>
</manifest>
        """

        manifest_path = os.path.join(self.scorm_dir, "imsmanifest.xml")
        with open(manifest_path, "w", encoding="utf-8") as file:
            file.write(contenido_imsmanifest)

    def empaquetar_scorm(self):
        zip_path = os.path.join(self.scorm_dir, 'paquete_scorm.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(self.scorm_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.scorm_dir))
        print("Empaquetado completado. Archivo ZIP guardado en:", zip_path)
        return zip_path

    def generar_paquete_scorm(self, config, seleccion):
        self.copiar_archivos_estaticos_y_config(config)
        self.generar_imsmanifest(seleccion)
        return self.empaquetar_scorm()