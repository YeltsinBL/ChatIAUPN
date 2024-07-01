# import sys
import torch
from TTS.api import TTS

# Obtener texto
# texto ="Sí, la universidad cuenta con un estacionamiento para bicicletas." #sys.argv[1]
# Cuda o CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
# Iniciar TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
def generar_Audio(texto,nro):

    archivo=f"tts_vits{nro}"
    # Generar .wav
    print(nro)
    tts.tts_to_file(text=texto, speaker_wav="speaker.wav", language="es", file_path=f"audios/{archivo}.wav")
    return archivo
