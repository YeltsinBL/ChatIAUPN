"""Generador de texto entrenado"""
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el tokenizador y el modelo entrenado
tokenizer = AutoTokenizer.from_pretrained(os.getcwd()+"/model_gpt_upn/")
model = AutoModelForCausalLM.from_pretrained(os.getcwd()+"/model_gpt_upn/")

# Asegurarse de que el modelo esté en modo evaluación
model.eval()

# Definir el dispositivo (GPU o CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Cargar las preguntas del corpus
with open('CorpusChatBot.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
preguntas_corpus = [line.split('|')[0].strip() for line in lines if '|' in line]

def calcular_similitud(pregunta1, pregunta2):
    # Cargar el modelo BERT para calcular similitud
    bert_model = AutoModel.from_pretrained('bert-base-uncased')
    bert_tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    bert_model.to(device)
    bert_model.eval()

    inputs1 = bert_tokenizer(pregunta1, return_tensors='pt', truncation=True, padding=True).to(device)
    inputs2 = bert_tokenizer(pregunta2, return_tensors='pt', truncation=True, padding=True).to(device)

    with torch.no_grad():
        outputs1 = bert_model(**inputs1).last_hidden_state.mean(dim=1)
        outputs2 = bert_model(**inputs2).last_hidden_state.mean(dim=1)

    similarity = cosine_similarity(outputs1.cpu().numpy(), outputs2.cpu().numpy())
    return similarity[0][0]

def encontrar_pregunta_similar(pregunta, umbral=0.7):
    """Encontrar la pregunta más similar en el corpus"""
    max_similitud = 0
    pregunta_similar = None

    for pregunta_corpus in preguntas_corpus:
        similitud = calcular_similitud(pregunta, pregunta_corpus)
        if similitud > max_similitud:
            max_similitud = similitud
            pregunta_similar = pregunta_corpus

    if max_similitud >= umbral:
        return pregunta_similar
    else:
        return None

def generar_respuestas(pregunta, adicional =" "):
    """Mostrar las respuestas generadas"""

    # prompt = "¿Puedo entrar con bicicleta?"
    inputs = tokenizer(pregunta, return_tensors="pt").to(device)

    # Generar las respuestas
    sample_outputs = model.generate(
        inputs['input_ids'],
        num_return_sequences=2,
        max_new_tokens=150,  # Ajusta el valor según sea necesario
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
        #print("responder",responder)
        # _,  respuesta = responder.split("?")
        separar_pregunta = responder.split("?")
        #print("separar_pregunta",separar_pregunta)
        # verificar espacio vacio
        respuesta_separada = [pregunta.strip() for pregunta in separar_pregunta if pregunta]
        verificar_pregunta=[]
        for dato in respuesta_separada:
            dato += "?" if dato[0:1]=="¿" else ""
            verificar_pregunta.append(dato)
        #print("verificar_pregunta",verificar_pregunta)
        #respuesta = " ".join((adicional.join(verificar_pregunta[1:]) \
        #            if len(verificar_pregunta) > 1 \
        #            else adicional.join(verificar_pregunta)\
        #                if len(verificar_pregunta) == 1\
        #                else "Lo siento, hubo un inconveniente al procesar la información.").split()[:150])
        #print("CANTIDAD verificar_pregunta",len(verificar_pregunta))
        if len(verificar_pregunta) > 1:
            preparar= " ".join(verificar_pregunta[1:])
            #print("Prepara > 1", preparar)
        else:
            if len(verificar_pregunta) == 1:
                preparar= " ".join(verificar_pregunta)
                #print("Prepara = 1", preparar)
            else:
                preparar= "Lo siento, hubo un inconveniente al procesar la información."
                #print("Prepara", preparar)
        preparar = adicional+preparar
        #print("SIMULAR Prepara",preparar)
        respuesta = " ".join(preparar.split()[:150])
        #print("respuesta",respuesta)
        #respuesta_filtrada = " ".join(respuesta.split()[:150])
        respuestas.append(respuesta)
    return respuestas
def respuestas_generadas(pregunta):
    """Verificar si la pregunta es igual o similar al corpus"""

    if pregunta in preguntas_corpus:
        respuestas = generar_respuestas(pregunta)
        return respuestas
    pregunta_similar = encontrar_pregunta_similar(pregunta)
    if pregunta_similar:
        respuestas = generar_respuestas(pregunta_similar, f"Capaz quisiste preguntar: '{pregunta_similar}' \n\n")
        return respuestas
    return ["Lo siento, no he logrado comprender tu pregunta. Pregunta de nuevo por favor."]

#respuestas_generadas()
