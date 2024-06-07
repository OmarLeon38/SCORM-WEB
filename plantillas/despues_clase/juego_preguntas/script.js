let currentQuestion = 0;
let questions = [];
let selectedOption;
let optionsEnabled = true;
let correctCount = 0;
let incorrectCount = 0;

document.addEventListener("DOMContentLoaded", function() {
    fetch('config.json')  // Asegúrate de que este archivo está configurado correctamente con preguntas
        .then(response => response.json())
        .then(data => {
            questions = data.questions;
            document.getElementById('quiz-title').textContent = data.title;
            showQuestion();
        });
});

function showQuestion() {
    optionsEnabled = true;
    document.getElementById('next-btn').disabled = true;
    const question = questions[currentQuestion];
    document.getElementById('question').textContent = question.question;
    const options = document.getElementById('options');
    options.innerHTML = '';
    question.options.forEach((option, index) => {
        const li = document.createElement('li');
        li.textContent = option;
        li.id = 'option-' + index;
        li.onclick = () => selectOption(li);
        options.appendChild(li);
    });
}

function selectOption(li) {
    if (!optionsEnabled) return;
    if (selectedOption) {
        selectedOption.classList.remove('selected');
    }
    selectedOption = li;
    selectedOption.classList.add('selected');
}

function confirmAnswer() {
    if (!selectedOption || !optionsEnabled) return;
    optionsEnabled = false;
    const correct = questions[currentQuestion].answer;
    const correctIndex = questions[currentQuestion].options.indexOf(correct);
    const correctOption = document.getElementById('option-' + correctIndex);

    // Se añade la verificación y se incrementa el contador correspondiente
    if (selectedOption.textContent === correct) {
        selectedOption.classList.add('correct');
        correctCount++;  // Incrementa el contador de respuestas correctas
    } else {
        selectedOption.classList.add('incorrect');
        correctOption.classList.add('correct');
        incorrectCount++;  // Incrementa el contador de respuestas incorrectas
    }

    document.getElementById('next-btn').disabled = false;
}


function nextQuestion() {
    currentQuestion++;
    if (currentQuestion < questions.length) {
        selectedOption = null;
        showQuestion();
    } else {
        document.getElementById('quiz-container').style.display = 'none';
        document.getElementById('results').style.display = 'block';
        document.getElementById('correct-count').textContent = `Correctas: ${correctCount}`;
        document.getElementById('incorrect-count').textContent = `Incorrectas: ${incorrectCount}`;
    }
}

function restartQuiz() {
    currentQuestion = 0;
    correctCount = 0;
    incorrectCount = 0;
    selectedOption = null;
    optionsEnabled = true;
    document.getElementById('results').style.display = 'none';
    document.getElementById('quiz-container').style.display = 'block';
    showQuestion();
}