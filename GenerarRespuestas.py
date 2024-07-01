import time
from transformers import AutoTokenizer, AutoModel,pipeline
import torch
import faiss

with open('corpusSincoma.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

documents =lines[1:2]
#print(documents)
#print("-----")
model_name = "sentence-transformers/paraphrase-xlm-r-multilingual-v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def embed_texts(texts):
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings

document_embeddings = embed_texts(documents).numpy()

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(document_embeddings)

id_to_document = {i: doc for i, doc in enumerate(documents)}

qa_model_name = "mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
qa_pipeline = pipeline("question-answering", model=qa_model_name, tokenizer=qa_model_name)

def answer_question(question):
    """Generar Respuestas"""
    query_embedding = embed_texts([question]).numpy()
    distances, indices = index.search(query_embedding, 1)

    #query = "cuándo empiezan las clases?"
    start_time = time.time()
    respuesta = []
    retrieved_docs = [(id_to_document[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
    result = qa_pipeline(question=question, context=retrieved_docs[0][0])
    score = round(float(result["score"]),3) #round(float_number, 2)
    if score >= 0.1:
        resp = result["answer"]
    else:
        resp = "Lo siento, no he logrado comprender tu pregunta. Pregunta de nuevo por favor."
    respuesta.append(resp)
    answer_time = time.time() - start_time
    print(f"Time taken to generate answer: {answer_time:.2f} seconds")
    return respuesta, score, round(answer_time,2)

#context = retrieved_docs[0][0]
#answer = answer_question(query, context)
#print(answer)
#print("-----")
