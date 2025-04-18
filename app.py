# # import os
# # #import langchain

# # from dotenv import load_dotenv



# # from langchain.document_loaders import PyPDFLoader
# # from langchain.embeddings import OpenAIEmbeddings
# # from langchain.vectorstores import FAISS
# # from langchain.chains import RetrievalQA
# # from langchain.chat_models import ChatOpenAI

# # import streamlit as st


# # ##### Configurar API da OpenAI

# # load_dotenv()
# # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# # ##### Criar pipeline RAG com LangChain

# # # Carrega dados
# # loader = PyPDFLoader("data/seu_arquivo.pdf")
# # docs = loader.load()

# # # Indexa com embeddings
# # embeddings = OpenAIEmbeddings()
# # db = FAISS.from_documents(docs, embeddings)

# # # Cria chatbot com RAG
# # retriever = db.as_retriever()
# # llm = ChatOpenAI(temperature=0.2)
# # qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)



# # ######   Criar interface no Streamlit  ##############

# # st.set_page_config(page_title="Chat RAG", layout="centered")
# # st.title("🤖 Chatbot com RAG")

# # if "messages" not in st.session_state:
# #     st.session_state.messages = []

# # for msg in st.session_state.messages:
# #     st.chat_message(msg["role"]).write(msg["content"])

# # prompt = st.chat_input("Digite sua pergunta...")
# # if prompt:
# #     st.session_state.messages.append({"role": "user", "content": prompt})
# #     st.chat_message("user").write(prompt)

# #     with st.spinner("Consultando..."):
# #         response = qa_chain.run(prompt)

# #     st.session_state.messages.append({"role": "assistant", "content": response})
# #     st.chat_message("assistant").write(response)

# import os
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.document_loaders.parsers import PDFMinerParser
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# from langchain.chat_models import ChatOpenAI
# import streamlit as st
# import tempfile
# from PyPDF2 import PdfReader
# from langchain.schema import Document
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from dotenv import load_dotenv

# import os
# import cohere
# from dotenv import load_dotenv
# from langchain.vectorstores import FAISS
# from langchain.embeddings.base import Embeddings

# # Função para extrair texto do PDF
# def extract_text_from_pdf(pdf_file):
#     reader = PdfReader(pdf_file)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
#     return text

# # Classe para representar os documentos extraídos
# class MyDocument(Document):
#     def __init__(self, content):
#         self.page_content = content


# # Função para criar documentos para FAISS
# def create_documents(text):
#     # Aqui criamos um objeto de documento para o FAISS
#     return [Document(page_content=text)]


# # Função para gerar embeddings usando o Cohere
# def obter_embeddings_com_cohere(textos):
#     client = cohere.Client(cohere_api_key)
#     response = client.embed(texts=textos)
#     embeddings = response.embeddings
#     return embeddings

# # Função para usar o FAISS com os embeddings obtidos do Cohere
# def criar_faiss_com_embeddings(docs):
#     embeddings = obter_embeddings_com_cohere([doc.page_content for doc in docs])
#     db = FAISS.from_documents(docs, embeddings)
#     return db




# # Configurar API da OpenAI com secrets
# #api_key = st.secrets["OPENAI_API_KEY"]

# # Criar pipeline RAG com LangChain
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # # Carregar e indexar documentos
# # uploaded_file = st.file_uploader("Carregue seu arquivo PDF", type="pdf")

# # if uploaded_file is not None:
# #     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
# #         tmp_file.write(uploaded_file.read())
# #         tmp_path = tmp_file.name

# # # Usa o caminho temporário no PyPDFLoader
# #     loader = PyPDFLoader(tmp_path)#, parser=PDFMinerParser())

# #Nova tentativa de carregamento
# # Interface de upload do arquivo PDF
# st.title("Carregue seu arquivo PDF")
# uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])

# if uploaded_file is not None:
#     try:
#         pdf_text = extract_text_from_pdf(uploaded_file)
#         st.write("Texto extraído com sucesso!")

#     # Agora criando os documentos
#         docs = create_documents(pdf_text)

#     # Indexando no FAISS
#         embeddings = OpenAIEmbeddings()
#         db = FAISS.from_documents(docs, embeddings)
#         st.write("Documento indexado com sucesso!")

#     except Exception as e:
#         st.error(f"Ocorreu um erro: {e}")




#     #docs = text
#     load_dotenv()

#     openai_api_key = os.getenv("OPENAI_API_KEY")

#     #print("API Key:", openai_api_key)

#     embeddings = OpenAIEmbeddings(openai_api_key=api_key)
#     db = FAISS.from_documents(docs, embeddings)


# # Configurar a chave de API do Cohere
#     cohere_api_key = os.getenv('COHERE_API_KEY')  # Certifique-se de que a chave está no .env




#     # Criar chatbot com RAG
#     retriever = db.as_retriever()
#     llm = ChatOpenAI(temperature=0.2, openai_api_key=api_key)
#     qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

#     st.title("🤖 Chatbot com RAG")

#     for msg in st.session_state.messages:
#         st.chat_message(msg["role"]).write(msg["content"])

#     prompt = st.chat_input("Digite sua pergunta...")
#     if prompt:
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         st.chat_message("user").write(prompt)

#         with st.spinner("Consultando..."):
#             response = qa_chain.run(prompt)

#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.chat_message("assistant").write(response)
# else:
#     st.warning("Por favor, carregue um arquivo PDF.")


import os
import cohere
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
from PyPDF2 import PdfReader
import tempfile

# Carregar variáveis de ambiente
load_dotenv()

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

# Função para criar documentos para FAISS
def create_documents(text):
    return [Document(page_content=text)]

# Função para gerar embeddings usando o Cohere
def obter_embeddings_com_cohere(textos):
    load_dotenv()
    #cohere_api_key = os.getenv("COHERE_API_KEY")  # Carregar chave API do Cohere
    
    CAK = "kIhP09qQgfqxJRlqc8ZJ9jdpQJYSAkCD3yZoYiVo"


    #if not cohere_api_key:
   #     raise ValueError(f"A chave de API do Cohere não está configurada corretamente:{cohere_api_key}" )
    
    client = cohere.Client(CAK)#cohere_api_key)  # Inicializa o cliente com a chave
    response = client.embed(texts=textos)
    embeddings = response.embeddings
    return embeddings

# Função para usar o FAISS com os embeddings obtidos do Cohere
def criar_faiss_com_embeddings(docs):
    embeddings = obter_embeddings_com_cohere([doc.page_content for doc in docs])
    db = FAISS.from_documents(docs, embeddings)
    return db

# Interface de upload do arquivo PDF
st.title("Carregue seu arquivo PDF")
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.write("Texto extraído com sucesso!")

        # Criando os documentos
        docs = create_documents(pdf_text)

        # Indexando no FAISS
        db = criar_faiss_com_embeddings(docs)
        st.write("Documento indexado com sucesso!")

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

    # Criar chatbot com RAG
    retriever = db.as_retriever()
    st.title("🤖 Chatbot com RAG")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    prompt = st.chat_input("Digite sua pergunta...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("Consultando..."):
            response = retriever.retrieve(prompt)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

else:
    st.warning("Por favor, carregue um arquivo PDF.")