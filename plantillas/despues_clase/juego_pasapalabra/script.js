document.addEventListener("DOMContentLoaded", function() {
    const configPath = 'config.json'; 
    fetch(configPath)
        .then(response => response.json())
        .then(config => {
            iniciarJuego(config);
        })
        .catch(error => console.error('Error al cargar la configuración:', error));
});

function iniciarJuego(config) {
    const bd_juego = config.preguntas;
    const total_preguntas = bd_juego.length;
    let cantidadAcertadas = 0;
    let numPreguntaActual = -1;
    const estadoPreguntas = new Array(total_preguntas).fill(0);
    let timeLeft = config.tiempo;

    const container = document.querySelector(".container");
    container.innerHTML = '';

    // Crear el elemento de tiempo dentro del contenedor antes de cualquier círculo
    const tiempo = document.createElement("span");
    tiempo.id = "tiempo";
    tiempo.innerText = timeLeft;
    tiempo.style.fontSize = "50px";  // Asegura que el tamaño del texto sea grande y visible
    tiempo.style.color = "black";  // Asegura que el color del texto sea visible
    container.appendChild(tiempo);

    bd_juego.forEach((item, index) => {
        const circle = document.createElement("div");
        circle.classList.add("circle");
        circle.textContent = item.letra;
        circle.id = item.letra;
        const angle = (index / total_preguntas) * Math.PI * 2 - (Math.PI / 2);
        const x = Math.round(95 + 120 * Math.cos(angle));
        const y = Math.round(95 + 120 * Math.sin(angle));
        circle.style.left = `${x}px`;
        circle.style.top = `${y}px`;
        container.appendChild(circle);
    });

    document.getElementById("comenzar").addEventListener("click", function() {
        document.getElementById("pantalla-inicio").style.display = "none";
        document.getElementById("pantalla-juego").style.display = "block";
        cargarPregunta();
        restarTiempo(config.tiempo);
    });

    function restarTiempo(timeLeft) {
        const countdown = setInterval(() => {
            timeLeft--;
            document.getElementById("tiempo").innerText = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(countdown);
                mostrarPantallaFinal();
            }
        }, 1000);
    }

    function cargarPregunta() {
        if (estadoPreguntas.indexOf(0) === -1) {
            mostrarPantallaFinal();
            return;  // Todas las preguntas han sido respondidas
        }

        do {
            numPreguntaActual = (numPreguntaActual + 1) % total_preguntas;
        } while (estadoPreguntas[numPreguntaActual] !== 0);

        const preguntaActual = bd_juego[numPreguntaActual];
        document.getElementById("letra-pregunta").textContent = preguntaActual.letra;
        document.getElementById("pregunta").textContent = preguntaActual.pregunta;
        document.querySelectorAll(".circle").forEach(circle => circle.classList.remove("pregunta-actual"));
        document.getElementById(preguntaActual.letra).classList.add("pregunta-actual");
    }

    function verificarRespuesta() {
        const respuesta = document.getElementById("respuesta").value.trim().toLowerCase();
        if (respuesta === "") {
            alert("Debes ingresar una respuesta");
        } else {
            controlarRespuesta(respuesta);
            document.getElementById("respuesta").value = ''; // Limpiar el input
            cargarPregunta(); // Cargar la siguiente pregunta
        }
    }

    document.getElementById("responder").addEventListener("click", verificarRespuesta);

    function controlarRespuesta(respuesta) {
        const preguntaActual = bd_juego[numPreguntaActual];
        if (respuesta === preguntaActual.respuesta.toLowerCase()) {
            cantidadAcertadas++;
            estadoPreguntas[numPreguntaActual] = 1;
            document.getElementById(preguntaActual.letra).classList.replace("pregunta-actual", "bien-respondida");
        } else {
            estadoPreguntas[numPreguntaActual] = 1;
            document.getElementById(preguntaActual.letra).classList.replace("pregunta-actual", "mal-respondida");
        }
    }

    function mostrarPantallaFinal() {
        document.getElementById("acertadas").textContent = cantidadAcertadas;
        document.getElementById("score").textContent = `${((cantidadAcertadas * 100) / total_preguntas).toFixed(1)}% de acierto`;
        document.getElementById("pantalla-juego").style.display = "none";
        document.getElementById("pantalla-final").style.display = "block";
    }

    document.getElementById("volver-a-jugar").addEventListener("click", function() {
        cantidadAcertadas = 0;
        estadoPreguntas.fill(0);
        numPreguntaActual = -1;
        timeLeft = config.tiempo;
        document.getElementById("tiempo").innerText = timeLeft;
        document.getElementById("pantalla-final").style.display = "none";
        document.getElementById("pantalla-juego").style.display = "block";
        document.querySelectorAll(".circle").forEach(c => c.classList.remove("bien-respondida", "mal-respondida"));
        restarTiempo(config.tiempo);
        cargarPregunta();
    });
}
