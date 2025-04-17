import os
#import langchain

from dotenv import load_dotenv



from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import streamlit as st


##### Configurar API da OpenAI

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

##### Criar pipeline RAG com LangChain

# Carrega dados
loader = PyPDFLoader("data/seu_arquivo.pdf")
docs = loader.load()

# Indexa com embeddings
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(docs, embeddings)

# Cria chatbot com RAG
retriever = db.as_retriever()
llm = ChatOpenAI(temperature=0.2)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)



######   Criar interface no Streamlit  ##############

st.set_page_config(page_title="Chat RAG", layout="centered")
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
        response = qa_chain.run(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)