
# import os
# import cohere
# from langchain_community.embeddings import CohereEmbeddings
# from dotenv import load_dotenv
# from langchain.embeddings.base import Embeddings


# load_dotenv()

# CAK = "kIhP09qQgfqxJRlqc8ZJ9jdpQJYSAkCD3yZoYiVo"
# client = cohere.Client(os.getenv(CAK))
# print(client)
# response = client.embed(texts=textos)
# embeddings = response.embeddings
# print(embeddings)

# cohere_api_key = os.getenv("COHERE_API_KEY")
# print(cohere_api_key)
# embeddings = CohereEmbeddings(cohere_api_key)
# print(embeddings)   
    # Criar o FAISS usando os documentos e embeddings
# db = FAISS.from_documents(docs, embeddings)
# PRINT(db)

import os
import cohere
from langchain_community.embeddings import CohereEmbeddings
from dotenv import load_dotenv
from langchain.embeddings.base import Embeddings
from langchain.embeddings.base import Embeddings
import cohere

class CohereEmbeddings(Embeddings):
    def __init__(self, cohere_api_key: str):
        self.client = cohere.Client(cohere_api_key)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embed(texts=texts, model="embed-english-v3.0")
        return response.embeddings

    def embed_query(self, text: str) -> list[float]:
        response = self.client.embed(texts=[text], model="embed-english-v3.0")
        return response.embeddings[0]

cohere_api_key = os.getenv("COHERE_API_KEY")
embedding_model = CohereEmbeddings(cohere_api_key)
db = FAISS.from_documents(docs, embedding_model)
retriever = db.as_retriever()