from transformers import AutoTokenizer, AutoModel,pipeline
import torch
import faiss
import numpy as np

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

#def retrieve(query, k=1):
#    query_embedding = embed_texts([query]).numpy()
#    distances, indices = index.search(query_embedding, k)
#    return [(id_to_document[idx], distances[0][i]) for i, idx in enumerate(indices[0])]

#query = "cuándo empiezan las clases?"
#retrieved_docs = retrieve(query, k=1)


#

qa_model_name = "mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es"
qa_pipeline = pipeline("question-answering", model=qa_model_name, tokenizer=qa_model_name)

def answer_question(question):
    query_embedding = embed_texts([question]).numpy()
    distances, indices = index.search(query_embedding, 1)

    #query = "cuándo empiezan las clases?"
    respuesta = []
    retrieved_docs = [(id_to_document[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
    result = qa_pipeline(question=question, context=retrieved_docs[0][0])
    resp = result["answer"]
    print("result type", type(resp))
    respuesta.append(resp)
    return respuesta

#context = retrieved_docs[0][0]
#answer = answer_question(query, context)
#print(answer)
#print("-----")
