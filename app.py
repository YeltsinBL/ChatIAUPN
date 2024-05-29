"""Aplicación Principal"""
import os
from flask import Flask, render_template, request, jsonify
from ChatbotUPN import encontrar_respuesta
from GenerarTexto import respuestas_generadas

app = Flask(__name__)
# port = int(os.environ.get("PORT", 5000))
@app.route('/', methods = ['GET', 'POST'])
def home():
    """Página principal HTML"""
    if request.method =='POST':
        resp =""
        if request.form["tipo_entrenado"].capitalize() =="True":
            resp = respuestas_generadas(request.form["mensaje"])
        else: resp= encontrar_respuesta(request.form["mensaje"])
        return jsonify({'fin': resp})
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
