import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

def cargar_corpus(ruta_archivo):
    preguntas_respuestas = []
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        for line in file:
            pregunta, respuesta = line.strip().split("|")
            preguntas_respuestas.append((pregunta.strip(), respuesta.strip()))
    return preguntas_respuestas
# ruta_archivo = os.getcwd()+"/CorpusChatBot.txt"
# corpus = cargar_corpus(ruta_archivo)

def preprocess(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('spanish'))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def encontrar_respuesta(input_text):
    input_tokens = preprocess(input_text)
    max_similarity = 0
    best_match = None
    for pregunta, respuesta in cargar_corpus(os.getcwd()+"/CorpusChatBot.txt"):
        pregunta_tokens = preprocess(pregunta)
        similarity = len(set(input_tokens) & set(pregunta_tokens))
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = respuesta
    return best_match
