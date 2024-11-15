const speakBtn = document.getElementById('speak-btn');
const conversationDiv = document.getElementById('conversation');

speakBtn.addEventListener('click', () => {
    // Configuración del reconocimiento de voz
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'es-ES';
    recognition.interimResults = false;

    recognition.start();

    recognition.onresult = (event) => {
        const userInput = event.results[0][0].transcript;
        addMessage('Usuario', userInput);

        // Enviar el texto del usuario al servidor
        fetch('/get_bot_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = data.bot_response;
            addMessage('Bot', botResponse);
            textToSpeech(botResponse);
        });
    };

    recognition.onerror = (event) => {
        console.error('Error en el reconocimiento de voz:', event.error);
    };
});

function addMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    conversationDiv.appendChild(messageDiv);
}

function textToSpeech(text) {
    const synthesis = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'es-ES';
    synthesis.speak(utterance);
}