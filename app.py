from flask import Flask, render_template, request
from chatbot import generate_response  # Importa la función desde chatbot.py

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["message"]
    response = generate_response(user_input)
    return response

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(debug=False, host="127.0.0.1", port=8080) 
