from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configurar la API de Gemini
genai.configure(api_key=os.environ["API_KEY"])

# Lista de palabras clave relacionadas con finanzas
FINANCIAL_KEYWORDS = ["finanzas", "economía", "inversiones", "mercados", "ahorros", "banca", "créditos", "impuestos", "Hola", "deuda", "como estas", "tasa de interes", "cuotas",]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    user_input = request.json['user_input']

    # Verificar si el tema es financiero
    if es_tema_financiero(user_input):
        # Llamar a la API de Gemini si es un tema financiero
        bot_response = call_gemini_api(user_input)
    else:
        # Mensaje predeterminado si no es un tema financiero
        bot_response = "Lo siento, solo puedo responder preguntas relacionadas con finanzas."

    return jsonify({'bot_response': bot_response})

def es_tema_financiero(prompt):
    """
    Comprueba si la entrada del usuario está relacionada con finanzas.
    """
    return any(keyword in prompt.lower() for keyword in FINANCIAL_KEYWORDS)

def call_gemini_api(user_input):
    """
    Llama a la API de Gemini para obtener una respuesta específica sobre finanzas.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Configurar el prompt para que se limite a temas financieros
    prompt = f"""
    Eres un asistente financiero experto. Solo responde preguntas relacionadas con temas como economía, 
    inversiones, impuestos, presupuestos, mercados y similares.
    Usuario: {user_input}
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)