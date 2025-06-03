# utils/llm_utils.py
import os
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .mongo_utils import get_database # Import from sibling module
import streamlit as st

@st.cache_resource
def get_ollama_llm():
    """Initializes the Ollama LLM client."""
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "phi3:mini")
    print(f"Initializing Ollama LLM with base_url={ollama_base_url} and model={ollama_model}")
    try:
        llm = Ollama(base_url=ollama_base_url, model=ollama_model)
        # You might want to add a simple test query here to ensure connection
        # llm.invoke("Test connection") 
        print("Ollama LLM initialized successfully.")
        return llm
    except Exception as e:
        st.error(f"Failed to initialize Ollama LLM at {ollama_base_url} with model {ollama_model}: {e}")
        print(f"Failed to initialize Ollama LLM: {e}")
        return None

@st.cache_data # Cache the collection names
def get_collection_names(_db): # Pass db object to make caching dependent on it
    """Fetches the list of collection names from the database."""
    if _db is None:
        return []
    try:
        names = _db.list_collection_names()
        print(f"Fetched collection names: {names}")
        return names
    except Exception as e:
        st.warning(f"Could not fetch collection names: {e}")
        print(f"Could not fetch collection names: {e}")
        return []

def create_llm_chain(llm, db):
    """Creates the Langchain pipeline (chain) for answering questions."""
    if llm is None or db is None:
        st.error("LLM or Database connection is not available to create the chain.")
        return None

    collection_names = get_collection_names(db)
    if not collection_names:
        st.warning("No collections found in the database. The LLM might not have context.")

    # Simple prompt template - providing collection names as context
    # More sophisticated approaches might involve retrieving relevant documents first (RAG)
    template = """
    Você é um assistente de IA especializado em responder perguntas sobre dados económicos brasileiros armazenados numa base de dados MongoDB.
    A base de dados (	{db_name}	) contém as seguintes coleções: {collection_list}
    
    Cada coleção contém documentos com campos como 'localidade', 'periodo', 'valor', 'atividade', 'tipo', etc., dependendo da coleção específica.
    
    Com base neste contexto e no seu conhecimento geral, responda à seguinte pergunta do utilizador de forma clara e concisa.
    Se a pergunta parecer pedir dados específicos que exigiriam uma consulta direta (ex: 'Qual o valor exato de X em Y?'), explique que você pode descrever os dados disponíveis e as coleções relevantes, mas não pode executar consultas diretas para obter valores específicos neste momento.
    
    Pergunta: {question}
    
    Resposta:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["question"],
        partial_variables={
            "db_name": db.name,
            "collection_list": ", ".join(collection_names) if collection_names else "Nenhuma coleção encontrada"
        }
    )

    # Create the chain using Langchain Expression Language (LCEL)
    chain = prompt | llm | StrOutputParser()
    print("Langchain chain created successfully.")
    return chain

# Example usage (optional, for testing):
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # Load .env for local testing
    
    test_db = get_database()
    test_llm = get_ollama_llm()
    
    if test_llm and test_db:
        test_chain = create_llm_chain(test_llm, test_db)
        if test_chain:
            print("\nTesting chain with a sample question...")
            try:
                response = test_chain.invoke({"question": "Quais coleções contêm dados sobre IPCA?"})
                print(f"Test Response:\n{response}")
            except Exception as e:
                print(f"Error invoking test chain: {e}")
        else:
            print("Failed to create test chain.")
    else:
        print("Failed to initialize LLM or DB for testing.")


