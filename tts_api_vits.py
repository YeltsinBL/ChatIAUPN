import sys
import torch
from TTS.api import TTS

# Obtener texto
# texto ="Sí, la universidad cuenta con un estacionamiento para bicicletas." #sys.argv[1]
def generar_Audio(texto,nro):
    # Cuda o CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Iniciar TTS
    tts = TTS("tts_models/es/css10/vits").to(device)

    archivo=f"tts_vits{nro}"
    # Generar .wav
    print(nro)
    tts.tts_to_file(text=texto, file_path=f"audios/{archivo}.wav")
    return archivo
