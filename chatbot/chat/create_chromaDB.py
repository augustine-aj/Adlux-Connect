import os
import json
import chromadb
from sentence_transformers import SentenceTransformer
# from chromadb.config import Settings
from chromadb.utils import embedding_functions
from datetime import datetime

client = chromadb.PersistentClient(path='appollo_chatbot_chroma2')
# model = SentenceTransformer('all-mpnet-base-v2')
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
model = SentenceTransformer('all-mpnet-base-v2')


def load_qanda_from_json(qanda_file_path):
    with open(qanda_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    qanda_pairs = []
    for key, items in data.items():
        for item in items:
            qanda_pairs.append({"question": item["question"], "answer": item["answer"]})
    return qanda_pairs


# Preprocess function
def preprocess(text):
    return text.lower()


def add_qanda_to_chroma(qanda_pairs):
    collection = client.create_collection(name="hospital_qanda2", metadata={"hnsw:space": "cosine"},
                                          embedding_function=sentence_transformer_ef)
    print('collection created.. ')
    for i, pair in enumerate(qanda_pairs):
        question = preprocess(pair["question"])
        answer = pair["answer"]

        if isinstance(answer, list):
            answer = "\n".join(answer)
        question_embedding = model.encode([question])[0].tolist()
        collection.add(
            ids=[f"qanda_{i}"],
            documents=[answer],
            metadatas=[{"source": f"qanda_{i}", "question": question}],
            embeddings=[question_embedding]
        )

    print("Q&A pairs added to Chroma collection successfully.")


def setup_qanda_db():
    qanda_file_path = ("C:/Users/augus/PycharmProjects/image_captioning/RAG DEMO/Real "
                       "data/appollo_gpt_generated_qanda_pair.json")
    qanda_pairs = load_qanda_from_json(qanda_file_path)
    print('Q&A file loaded successfully.')
    add_qanda_to_chroma(qanda_pairs)


def add_session_data(user_name, s_ID, query):
    session_client = chromadb.PersistentClient(path=f"{user_name}")
    if not session_client:
        print("session_client is missing")
        return

    collection = session_client.get_or_create_collection(name=f"{user_name}_{s_ID}",
                                                         metadata={"hnsw:space": "cosine"},
                                                         embedding_function=sentence_transformer_ef)

    collection.add(
        ids=[f"{user_name}_{s_ID}"],
        documents=[query],
        metadatas=[
            {
                "session_id": s_ID,
                "user_name": user_name,
                "query": query,
                "time_stamp": datetime.now().isoformat()
            }
        ]
    )

    print(f"Collection created and added data. collection name : {user_name}_{s_ID}")


def update_session_data(user_name, s_ID, message):
    session_client = chromadb.PersistentClient(path=f"{user_name}")
    collection = session_client.get_collection(name=f"{user_name}_{s_ID}")

    collection.add(
        ids=[f"{user_name}_{s_ID}"],
        documents=[message],
        metadatas=[{
            "message": message,
        }]
    )

    print("Message data added to ChromaDB collection successfully.")

# setup_chroma_db()
