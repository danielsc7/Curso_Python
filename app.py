# import os
# #import langchain

# from dotenv import load_dotenv



# from langchain.document_loaders import PyPDFLoader
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# from langchain.chat_models import ChatOpenAI

# import streamlit as st


# ##### Configurar API da OpenAI

# load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ##### Criar pipeline RAG com LangChain

# # Carrega dados
# loader = PyPDFLoader("data/seu_arquivo.pdf")
# docs = loader.load()

# # Indexa com embeddings
# embeddings = OpenAIEmbeddings()
# db = FAISS.from_documents(docs, embeddings)

# # Cria chatbot com RAG
# retriever = db.as_retriever()
# llm = ChatOpenAI(temperature=0.2)
# qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)



# ######   Criar interface no Streamlit  ##############

# st.set_page_config(page_title="Chat RAG", layout="centered")
# st.title("🤖 Chatbot com RAG")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# prompt = st.chat_input("Digite sua pergunta...")
# if prompt:
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     with st.spinner("Consultando..."):
#         response = qa_chain.run(prompt)

#     st.session_state.messages.append({"role": "assistant", "content": response})
#     st.chat_message("assistant").write(response)

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers import PDFMinerParser
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import streamlit as st
import tempfile
from PyPDF2 import PdfReader
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Função para extrair texto do PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Classe para representar os documentos extraídos
class MyDocument(Document):
    def __init__(self, content):
        self.page_content = content



# Configurar API da OpenAI com secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Criar pipeline RAG com LangChain
if "messages" not in st.session_state:
    st.session_state.messages = []

# # Carregar e indexar documentos
# uploaded_file = st.file_uploader("Carregue seu arquivo PDF", type="pdf")

# if uploaded_file is not None:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         tmp_path = tmp_file.name

# # Usa o caminho temporário no PyPDFLoader
#     loader = PyPDFLoader(tmp_path)#, parser=PDFMinerParser())

#Nova tentativa de carregamento
# Interface de upload do arquivo PDF
st.title("Carregue seu arquivo PDF")
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        # Lê o conteúdo do PDF
        text = extract_text_from_pdf(uploaded_file)

        # Cria documentos para FAISS (formato adequado)
        docs = [MyDocument(content=text)]

        # Definindo o modelo de embeddings
        embeddings = OpenAIEmbeddings()

        # Cria o índice FAISS a partir dos documentos
        db = FAISS.from_documents(docs, embeddings)

        st.subheader("Conteúdo do PDF:")
        st.text_area("Texto extraído:", text, height=300)

        st.success("Texto extraído com sucesso e FAISS indexado!")

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")




    docs = text

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.from_documents(docs, embeddings)

    # Criar chatbot com RAG
    retriever = db.as_retriever()
    llm = ChatOpenAI(temperature=0.2, openai_api_key=api_key)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    st.title("🤖 Chatbot com RAG")

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
