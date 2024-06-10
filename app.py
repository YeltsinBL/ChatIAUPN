"""Aplicación Principal"""
# import os
from flask import Flask, render_template, request, jsonify,send_file, Response
from ChatbotUPN import encontrar_respuesta
from GenerarTexto import respuestas_generadas
from tts_api_vits import generar_Audio

app = Flask(__name__)
# port = int(os.environ.get("PORT", 5000))
@app.route('/', methods = ['GET', 'POST'])
def home():
    """Página principal HTML"""
    if request.method =='POST':
        resp =""
        if request.form["tipo_entrenado"].capitalize() =="True":
            resp = respuestas_generadas(request.form["mensaje"])
        else:
            resp= encontrar_respuesta(request.form["mensaje"])
            audio = generar_Audio(resp,request.form["numero_pregunta"])
        return jsonify({'fin': resp, 'audio':audio})
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
