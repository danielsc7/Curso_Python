#Projeto de chatbot construído usando RAG com a ferramenta Cohere, disponibilizado no Streamlit

import os
import cohere
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain_community.embeddings import CohereEmbeddings  # Usar CohereEmbeddings do LangChain
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.base import Embeddings
import streamlit as st
import tempfile
from PyPDF2 import PdfReader
from langchain.schema import Document
import cohere
from langchain.llms.base import LLM
from typing import Optional, List


load_dotenv()


class CohereLLM(LLM):
    def __init__(self, cohere_api_key: str, model: str = "command-r", temperature: float = 0.3):
        self.client = cohere.Client(cohere_api_key)
        self.model = model
        self.temperature = temperature

    @property
    def _llm_type(self) -> str:
        return "cohere"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=500,
            stop_sequences=stop or [],
        )
        return response.generations[0].text.strip()

# Função para extrair texto do PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Função para criar documentos para FAISS
def create_documents(text):
    return [Document(page_content=text)]

# Função para usar o FAISS com os embeddings obtidos do Cohere
def criar_faiss_com_embeddings(docs):
    load_dotenv()
    CAK = "kIhP09qQgfqxJRlqc8ZJ9jdpQJYSAkCD3yZoYiVo"
    # Usar CohereEmbeddings do LangChain para gerar os embeddings
    embeddings = CohereEmbeddings(cohere_api_key=CAK)
    
    # Criar o FAISS usando os documentos e embeddings
    db = FAISS.from_documents(docs, embeddings)
    return db

# Carregar variáveis do arquivo .env
load_dotenv()

# Interface de upload do arquivo PDF
st.title("Carregue seu arquivo PDF")
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.write("Texto extraído com sucesso!")

        # Criando os documentos para FAISS
        docs = create_documents(pdf_text)

        # Gerar o FAISS com os embeddings do Cohere
        db = criar_faiss_com_embeddings(docs)
        st.write("Documento indexado com sucesso!")

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

    # Criar o retriever e o modelo para o chatbot
    retriever = db.as_retriever()
    llm = CohereLLM(cohere_api_key=cohere_api_key, temperature=0.2)  # Usando Cohere
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Criar interface no Streamlit
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    prompt = st.chat_input("Digite sua pergunta...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Consultando..."):
            response = qa_chain.run(prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

else:
    st.warning("Por favor, carregue um arquivo PDF.")
