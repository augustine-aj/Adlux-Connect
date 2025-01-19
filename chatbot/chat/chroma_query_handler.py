# from chromadb import Client
from sentence_transformers import SentenceTransformer
import chromadb
import os
import pandas as pd
from chat import create_chromaDB

# model = SentenceTransformer('all-mpnet-base-v2')
model = None
client = None


def setup_chroma_client():
    global client, model
    model = SentenceTransformer('all-mpnet-base-v2')
    client = chromadb.PersistentClient(path="chat/appollo_chatbot_chroma2")
    if not client:
        print("client is missing. ")


def get_query_embedding(query):
    query = query.lower()
    return model.encode([query])[0]


def retrieve_documents(query, top_k=3):
    try:
        if not client:
            print('Check the client path.. ')
            return {'documents': []}
        query_embedding = get_query_embedding(query)
        collection = client.get_collection("hospital_qanda2")
        if not collection:
            print("Collection not found.")
            return {"documents": []}
        print('searching for results')
        # results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        top_k_results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        print(f"Cosine results are{top_k_results['documents'][0]}\nSimilarity Scores: {top_k_results['distances'][0]}")
        print(
            f"Choosing the result : {top_k_results['documents'][0][2]}\nCosine Similarity score : "
            f"{top_k_results['distances'][0][2]}")

        """documents = top_k_results['documents'][0]
        distances = top_k_results['distances'][0]
        results = [{'document': documents[i], 'distance': distances[i]} for i in range(len(documents))]
        print(results)
        results_df = pd.DataFrame(results)
        results_df_sorted = results_df.sort_values(by='distance', ascending=False)
        print(f'{results_df_sorted = }')"""

        print('initialising l2 euclidean distance,,,,')
        client2 = chromadb.PersistentClient(path="appollo_chatbot_chroma")
        query_embedding = get_query_embedding(query)
        collection = client2.get_collection("hospital_qanda")
        if not collection:
            print("Collection not found.")
            return {"documents": []}
        print('searching for results')
        # results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        top_k_results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        # print(f"Cosine results are{top_k_results}")
        print(
            f"Euclidean results are{top_k_results['documents'][0]}\nSimilarity Scores: {top_k_results['distances'][0]}")
        print(
            f"Choosing the result {top_k_results['documents'][0][2]}\nEuclidean Similarity score :"
            f" {top_k_results['distances'][0][2]}")
        return top_k_results['documents'][0][2]
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return {"documents": []}

        # start from order the result by descending order of distances.
        # createa a similarity score bar low, med, high.
        # Reference link : https://chatgpt.com/share/6734d532-42ec-8003-91b4-b40c4f1cfbf1


def retrieve_session_data(user_name, s_ID, query=None, top_k=3):
    session_client = chromadb.PersistentClient(path=f"{user_name}")
    collection = session_client.get_collection(name=f"{user_name}_{s_ID}")

    if query:
        session_data = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        print(f'{session_data = }')
        return session_data
    else:
        session_data = collection.query()
        print(f'{session_data = }')
        return session_data


setup_chroma_client()
last_results = []

"""while True:
    user_name = input("user name : ")
    s_ID = input("Session ID : ")
    user_query = input("Enter a query: ")
    chroma_db.add_session_data(user_name, s_ID, user_query)
    result = retrieve_documents(user_query, top_k=3)
    last_results.append(result)
    if result:
        chroma_db.update_session_data(user_name, s_ID, result)
    retrieve_session_data(user_name, s_ID)
    print(f"{user_query = }")
    print('top result is : ', result['document'][0])
    print('Similarity Score is : ', result['distance'][0])"""
