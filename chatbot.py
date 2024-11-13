import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# Ejemplo de corpus de respuestas del chatbot
corpus = [
    "Hola, ¿en qué puedo ayudarte?",
    "servicios,¿Cuál es tu pregunta sobre nuestro servicio?",
    "información,¿Para más información, visita nuestra página web.?",
    "Gracias por comunicarte con nosotros.",
    "Lo siento, no tengo una respuesta para eso."
]

def preprocess_input(text):
    # Preprocesa el texto de entrada
    tokens = nltk.word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum()]
    return ' '.join(tokens)

def generate_response(user_input):
    user_input = preprocess_input(user_input)
    corpus.append(user_input)  # Añadimos la entrada del usuario al corpus temporalmente
    
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(corpus)
    
    # Calculamos la similitud de coseno entre la entrada y el corpus
    similarity = cosine_similarity(tfidf[-1], tfidf)
    index = similarity.argsort()[0][-2]
    
    corpus.pop()  # Eliminamos la entrada del usuario del corpus

    # Si la similitud es muy baja, responde con un mensaje de desconocimiento
    if similarity[0][index] < 0.2:
        return "Lo siento, no tengo una respuesta para eso."
    else:
        return corpus[index]
