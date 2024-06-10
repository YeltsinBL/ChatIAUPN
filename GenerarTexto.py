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

    # prompt = f"<|startoftext|>{pregunta}|<|endoftext|>"
    # Tokenizar el prompt
    # generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
    # generated = generated.to(device)

    # prompt = "¿Puedo entrar con bicicleta?"
    inputs = tokenizer(pregunta, return_tensors="pt").to(device)

    # Generar las respuestas
    sample_outputs = model.generate(
        inputs['input_ids'],
        num_return_sequences=1,
        max_length=100,  # Ajusta el valor según sea necesario
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id
    )
    respuestas=[]
    for _, sample_output in enumerate(sample_outputs):
        responder=tokenizer.decode(sample_output, skip_special_tokens=True)
        print("responder",responder)
        # _,  respuesta = responder.split("?")
        separar_pregunta = responder.split("?")
        print("separar_pregunta",separar_pregunta)
        # verificar espacio vacio
        respuesta_separada = [pregunta.strip() for pregunta in separar_pregunta if pregunta]
        verificar_pregunta=[]
        for dato in respuesta_separada:
            dato += "?" if dato[0:1]=="¿" else ""
            verificar_pregunta.append(dato)
        print("verificar_pregunta",verificar_pregunta)
        respuesta = " ".join(separar_pregunta[1:]) \
                    if len(separar_pregunta) > 1 \
                    else "Opps! Ha ocurrido un error, por favor intente de nuevo"
        print("respuesta",respuesta)
        respuestas.append(respuesta)
    return respuestas

#respuestas_generadas()
