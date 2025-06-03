# app.py
import streamlit as st
import os
from dotenv import load_dotenv

# Import utility functions
from utils.mongo_utils import get_database
from utils.llm_utils import get_ollama_llm, create_llm_chain

# Load environment variables from .env file
# Make sure to create a .env file from .env.example and fill in your details
load_dotenv()

# --- Configuration (Load from Environment Variables) ---
# Already loaded by load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini") # Get model name for display

# --- Streamlit App Layout ---
st.set_page_config(page_title="FecomDB Q&A", layout="wide")

st.title(" Perguntas e Respostas sobre Dados Económicos (FecomDB)")
st.caption(f"Utilizando o modelo LLM: {OLLAMA_MODEL} via Ollama e dados do MongoDB Atlas ({MONGO_DB_NAME})")

# --- Check Environment Variables ---
if not MONGO_URI or not MONGO_DB_NAME:
    st.error("Erro: Variáveis de ambiente MONGO_URI ou MONGO_DB_NAME não configuradas.")
    st.info("Por favor, copie `.env.example` para `.env` e preencha as suas credenciais do MongoDB Atlas.")
    st.stop()

# --- Initialize Connections and Pipeline ---
# Use context managers or ensure cleanup if needed, but Streamlit caching helps
with st.spinner("Conectando ao MongoDB..."):
    db = get_database() # Uses st.cache_resource

with st.spinner(f"Inicializando LLM ({OLLAMA_MODEL})..."):
    llm = get_ollama_llm() # Uses st.cache_resource

langchain_chain = None
if db is not None and llm is not None:
    with st.spinner("Criando pipeline de processamento..."):
        langchain_chain = create_llm_chain(llm, db)
else:
    st.error("Falha ao inicializar a conexão com o banco de dados ou o LLM. Verifique as configurações e logs.")
    # Optionally display specific errors from db or llm initialization if they were captured
    st.stop()

if not langchain_chain:
    st.error("Falha ao criar a pipeline Langchain. Verifique os logs.")
    st.stop()

st.success("Pronto para receber perguntas!")

# --- User Input ---
st.sidebar.header("Informações")
st.sidebar.info("Faça perguntas em linguagem natural sobre os dados económicos contidos nas coleções do MongoDB.")
# Add collection list to sidebar for user reference
try:
    collection_names = db.list_collection_names()
    st.sidebar.subheader("Coleções Disponíveis:")
    st.sidebar.json(collection_names)
except Exception as e:
    st.sidebar.warning(f"Não foi possível listar as coleções: {e}")

st.header("Faça a sua pergunta sobre os dados económicos:")
user_query = st.text_input("Sua pergunta:", key="user_query", placeholder="Ex: Quais coleções possuem dados sobre o IPCA?")

# --- Query Processing and Output ---
if st.button("Perguntar", key="ask_button"):
    if user_query:
        if langchain_chain:
            with st.spinner("Consultando o LLM..."):
                try:
                    response = langchain_chain.invoke({"question": user_query})
                    st.markdown("**Resposta:**")
                    st.write(response)
                except Exception as e:
                    st.error(f"Erro ao processar a pergunta: {e}")
                    print(f"Error invoking chain: {e}") # Log error to console
        else:
            st.error("A pipeline Langchain não está disponível.")
    else:
        st.warning("Por favor, insira uma pergunta.")


