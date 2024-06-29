"""Aplicación Principal"""
# import os
from flask import Flask, render_template, request, jsonify, Response, send_file, render_template_string
from ChatbotUPN import encontrar_respuesta
from GenerarTexto import respuestas_generadas
from GenerarRespuestas import answer_question
from tts_api_vits import generar_Audio
import pdfkit
import io
import logging

# from weasyprint import HTML
# Debugging by enabling pdfkit logging
options = {
    'quiet': ''
}
app = Flask(__name__)
# port = int(os.environ.get("PORT", 5000))


@app.route('/', methods=['GET', 'POST'])
def home():
    """Página principal HTML"""
    if request.method == 'POST':
        resp = ""
        if request.form["tipo_entrenado"].capitalize() == "True":
            #resp = respuestas_generadas(request.form["mensaje"])
            print("Respuestas")
            resp = answer_question(request.form["mensaje"])
            print("resp", resp)
            print("Audios")
            audio = []
            for index, res in enumerate(resp):
                print(index,res)
                audio.append(generar_Audio(
                    res, f"{request.form['numero_pregunta']}_{index}"))
        else:
            resp = encontrar_respuesta(request.form["mensaje"])
            audio = generar_Audio(resp, request.form["numero_pregunta"])
        return jsonify({'fin': resp, 'audio': audio})
    return render_template('index.html')


@app.route("/wav/<filename>")
def streamwav(filename):
    def generate():
        with open(f"audios/{filename}.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")


if __name__ == '__main__':
    app.run()
