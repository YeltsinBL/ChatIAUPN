"""Aplicación Principal"""
# import os
from flask import Flask, render_template, request, jsonify, Response, send_file, render_template_string
from ChatbotUPN import encontrar_respuesta
from GenerarTexto import respuestas_generadas
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
@app.route('/', methods = ['GET', 'POST'])
def home():
    """Página principal HTML"""
    if request.method =='POST':
        resp =""
        if request.form["tipo_entrenado"].capitalize() =="True":
            resp = respuestas_generadas(request.form["mensaje"])
            audio=""
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
@app.route("/pdf", methods = ['POST'])
def genera_pdf():
    """Generar PDF de las preguntas"""
    logging.basicConfig(level=logging.DEBUG)
    html = render_template('preview.html', datos=[{"pregunta":"Donde esta la biblioteca", "respuesta":"Esta en la uni xd"}])
    # print(html)
    try:
        ruta_wkhtmlpdf= r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config_pdfkit = pdfkit.configuration(wkhtmltopdf = ruta_wkhtmlpdf)
        pdf= pdfkit.from_string(html, False, configuration=config_pdfkit, options=options)
        #pdf= pdfkit.from_url(f'{request.host_url}pdf_view', configuration=config_pdfkit)
        #pdf=pdfkit.from_string(render_template('preview.html',datos=[{"pregunta":"Donde esta la biblioteca", "respuesta":"Esta en la uni xd"}]), False,configuration=config_pdfkit)
        print("Llegó")
        return send_file(io.BytesIO(pdf), mimetype='application/pdf',
                        as_attachment=True, download_name='PDF_ChatInteligenteUPN')
    except OSError as e:
        logging.error(f"Error generating PDF: {e}")
        return "Error generating PDF", 500

@app.route("/pdf_view", methods = ['GET', 'POST'])
def genera_pdf_view():
    """Vista previa"""
    return render_template('preview.html',datos=[{"pregunta":"Donde esta la biblioteca","respuesta":"Esta en la uni xd"}])
@app.route("/pdf_view_param/<data>", methods = ['GET', 'POST'])
def genera_pdf_view_param(data):
    """Vista previa"""
    print(data)
    return render_template('preview.html',datos=data)

if __name__ == '__main__':
    app.run()
