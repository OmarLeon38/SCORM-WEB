document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('generar-contenido')) {
        document.getElementById('generar-contenido').addEventListener('click', function() {
            const tema = document.getElementById('tema').value;
            const objetivo_general = document.getElementById('objetivo-general').value;
            const objetivo_antes = document.getElementById('objetivo-antes').value;
            const objetivo_durante = document.getElementById('objetivo-durante').value;
            const objetivo_despues = document.getElementById('objetivo-despues').value;
            const seleccion = {
                antes: [],
                durante: [],
                despues: []
            };
            document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
                if (checkbox.checked) {
                    if (checkbox.value.startsWith('motivacion') || checkbox.value.startsWith('objetivos') || checkbox.value.startsWith('preguntas') || checkbox.value.startsWith('introduccion') || checkbox.value.startsWith('video') || checkbox.value.startsWith('cuestionario_conocimientos_previos') || checkbox.value.startsWith('conceptos')) {
                        seleccion.antes.push(checkbox.value);
                    } else if (checkbox.value.startsWith('contenido') || checkbox.value.startsWith('ejemplos') || checkbox.value.startsWith('tarea_individual') || checkbox.value.startsWith('tarea_grupal') || checkbox.value.startsWith('herramientas') || checkbox.value.startsWith('ejercicios_programacion') || checkbox.value.startsWith('ejercicios_completar_codigo') || checkbox.value.startsWith('ejercicios_corregir_codigo') || checkbox.value.startsWith('proyecto')) {
                        seleccion.durante.push(checkbox.value);
                    } else if (checkbox.value.startsWith('cuestionario_final') || checkbox.value.startsWith('ejercicios_practicar') || checkbox.value.startsWith('resumen_final') || checkbox.value.starts.with('tarea_despues_clase') || checkbox.value.startsWith('recomendacion_libros') || checkbox.value.startsWith('aplicacion_problemas_reales')) {
                        seleccion.despues.push(checkbox.value);
                    }
                }
            });
            console.log('Selección:', seleccion);
            // Mostrar la barra de carga y animarla
            const progressBar = document.querySelector('.progress-bar');
            progressBar.style.width = '0%';
            progressBar.classList.add('progress-bar-animated');
            let width = 0;
            const interval = setInterval(() => {
                width += 1;
                progressBar.style.width = width + '%';
                if (width >= 90) {
                    clearInterval(interval);
                }
            }, 100);
            fetch('/generar_contenido', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tema: tema,
                    objetivo_general: objetivo_general,
                    objetivo_antes: objetivo_antes,
                    objetivo_durante: objetivo_durante,
                    objetivo_despues: objetivo_despues,
                    seleccion: seleccion
                })
            })
            .then(response => response.json())
            .then(data => {
                clearInterval(interval);
                progressBar.style.width = '100%';
                progressBar.classList.remove('progress-bar-animated');
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    window.location.href = data.redirect_url;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                clearInterval(interval);
                progressBar.style.width = '100%';
                progressBar.classList.remove('progress-bar-animated');
                alert('Ocurrió un error al generar el contenido.');
            });
        });
    }
    if (document.getElementById('confirmar-contenido')) {
        document.getElementById('confirmar-contenido').addEventListener('click', function() {
            const divs = document.querySelectorAll('div[contenteditable]');
            const contenidoEditado = {};
            divs.forEach(function(div) {
                const sectionTitle = div.previousElementSibling.textContent.toLowerCase().replace(/ /g, '_');
                contenidoEditado[sectionTitle] = div.innerHTML;
            });
            fetch('/confirmar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contenido: contenidoEditado,
                    seleccion: {
                        antes: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(input => input.value.startsWith('motivacion') || input.value.startsWith('objetivos') || input.value.startsWith('preguntas') || input.value.startsWith('introduccion') || input.value.startsWith('video') || input.value.startsWith('cuestionario_conocimientos_previos') || input.value.startsWith('conceptos')).map(input => input.value),
                        durante: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(input => input.value.startsWith('contenido') || input.value.startsWith('ejemplos') || input.value.startsWith('tarea_individual') || input.value.startsWith('tarea_grupal') || input.value.startsWith('herramientas') || input.value.startsWith('ejercicios_programacion') || input.value.starts.with('ejercicios_completar_codigo') || input.value.startsWith('ejercicios_corregir_codigo') || input.value.startsWith('proyecto')).map(input => input.value),
                        despues: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(input => input.value.startsWith('cuestionario_final') || input.value.startsWith('ejercicios_practicar') || input.value.startsWith('resumen_final') || input.value.startsWith('tarea_despues_clase') || input.value.startsWith('recomendacion_libros') || input.value.startsWith('aplicacion_problemas_reales')).map(input => input.value)
                    }
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'Error') {
                    alert('Error: ' + data.message);
                } else {
                    alert(data.status);
                    if (data.ruta) {
                        window.location.href = data.ruta;
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});