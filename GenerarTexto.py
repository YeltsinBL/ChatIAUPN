"""Generador de texto entrenado"""
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Cargar el tokenizador y el modelo entrenado
tokenizer = AutoTokenizer.from_pretrained(os.getcwd()+"/model_gpt_upn/")
model = AutoModelForCausalLM.from_pretrained(os.getcwd()+"/model_gpt_upn/")

# Asegurarse de que el modelo esté en modo evaluación
model.eval()

# Definir el dispositivo (GPU o CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def respuestas_generadas(pregunta):
    """Mostrar las respuestas generadas"""

    prompt = f"<|startoftext|>{pregunta}|<|endoftext|>"
    # Tokenizar el prompt
    generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
    generated = generated.to(device)

    # Generar las respuestas
    sample_outputs = model.generate(
        generated,
        num_return_sequences=3,
        max_length=300,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7  # Ajusta este valor según sea necesario
    )
    respuestas=[]
    for _, sample_output in enumerate(sample_outputs):
        responder=tokenizer.decode(sample_output, skip_special_tokens=True)
        _,  respuesta = responder.strip().split("|")
        respuestas.append((respuesta.strip()))
    return respuestas

#respuestas_generadas()
