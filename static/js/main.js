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
            if (checkbox.value.startsWith('resumen_') || checkbox.value.startsWith('video_') || checkbox.value.startsWith('objetivos_') || checkbox.value.startsWith('preguntas_') || checkbox.value.startsWith('cuestionario') || checkbox.value.startsWith('motivacion')) {
                seleccion.antes.push(checkbox.value);
            } else if (checkbox.value.startsWith('contenido_') || checkbox.value.startsWith('ejercicios_') || checkbox.value.startsWith('ejemplos_') || checkbox.value.startsWith('juego_') || checkbox.value.startswith('trabajo_') || checkbox.value.startsWith('herramientas_')) {
                seleccion.durante.push(checkbox.value);
            } else {
                seleccion.despues.push(checkbox.value);
            }
        }
    });

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
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            const contenidoGenerado = document.getElementById('contenido-generado');
            contenidoGenerado.innerHTML = '<h2>Contenido Generado</h2>';
            for (const section in data.contenido) {
                contenidoGenerado.innerHTML += `<h3>${section.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</h3>`;
                contenidoGenerado.innerHTML += `<div contenteditable='true' class='border p-2 mb-3'>${data.contenido[section]}</div>`;
            }
            document.getElementById('confirmar-contenido').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

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
                antes: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(input => input.value.startsWith('resumen_') || input.value.startsWith('video_') || input.value.startsWith('objetivos_') || input.value.startsWith('preguntas_') || input.value.startsWith('cuestionario') || input.value.startsWith('motivacion')).map(input => input.value),
                durante: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(input => input.value.startsWith('contenido_') || input.value.startsWith('ejercicios_') || input.value.startsWith('ejemplos_') || input.value.startsWith('juego_') || input.value.startsWith('trabajo_') || input.value.startsWith('herramientas_')).map(input => input.value),
                despues: Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).filter(input => input.value.startsWith('resumen_clase') || input.value.startsWith('cuestionario_despues') || input.value.startsWith('trabajo_despues_clase') || input.value.startsWith('recomendacion_libros') || input.value.startsWith('recomendaciones') || input.value.startsWith('ejercicios_practicar')).map(input => input.value)
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