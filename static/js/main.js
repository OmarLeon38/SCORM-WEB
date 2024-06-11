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
                    if (checkbox.value.startsWith('motivacion') || checkbox.value.startsWith('objetivos') || checkbox.value.startsWith('preguntas') || checkbox.value.startsWith('introduccion') || checkbox.value.startsarts('video') || checkbox.value.startsarts('cuestionario_conocimientos_previos') || checkbox.value.startsarts('conceptos')) {
                        seleccion.antes.push(checkbox.value);
                    } else if (checkbox.value.startsarts('contenido') || checkbox.value.startsarts('ejemplos') || checkbox.value.startsarts('tarea_individual') || checkbox.value.startsarts('tarea_grupal') || checkbox.value.startsarts('herramientas') || checkbox.value.startsarts('ejercicios_programacion') || checkbox.value.startsarts('ejercicios_completar_codigo') || checkbox.value.startsarts('ejercicios_corregir_codigo') || checkbox.value.startsarts('proyecto')) {
                        seleccion.durante.push(checkbox.value);
                    } else if (checkbox.value.startsarts('cuestionario_final') || checkbox.value.startsarts('ejercicios_practicar') || checkbox.value.startsarts('resumen_final') || checkbox.value.startsarts('tarea_despues_clase') || checkbox.value.startsarts('recomendacion_libros') || checkbox.value.startsarts('aplicacion_problemas_reales')) {
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
                alert('Error al generar el contenido: ' + error.message);
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
                        antes: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(input => input.value.startsarts('motivacion') || input.value.startsarts('objetivos') || input.value.startsarts('preguntas') || input.value.startsarts('introduccion') || input.value.startsarts('video') || input.value.startsarts('cuestionario_conocimientos_previos') || input.value.startsarts('conceptos')).map(input => input.value),
                        durante: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(input => input.value.startsarts('contenido') || input.value.startsarts('ejemplos') || input.value.startsarts('tarea_individual') || input.value.startsarts('tarea_grupal') || input.value.startsarts('herramientas') || input.value.startsarts('ejercicios_programacion') || input.value.startsarts('ejercicios_completar_codigo') || input.value.startsarts('ejercicios_corregir_codigo') || input.value.startsarts('proyecto')).map(input => input.value),
                        despues: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(input => input.value.startsarts('cuestionario_final') || input.value.startsarts('ejercicios_practicar') || input.value.startsarts('resumen_final') || input.value.startsarts('tarea_despues_clase') || input.value.startsarts('recomendacion_libros') || input.value.startsarts('aplicacion_problemas_reales')).map(input => input.value)
                    }
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'Error') {
                    alert('Error: ' + data.message);
                } else {
                    alert(data.status + (data.ruta ? '\nRuta: ' + data.ruta : ''));
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});