# Projeto LLM para Consulta de Dados Económicos (FecomDB)

Este projeto implementa uma aplicação web simples utilizando Streamlit para permitir que os utilizadores façam perguntas em linguagem natural sobre dados económicos armazenados numa base de dados MongoDB Atlas. A aplicação utiliza Langchain para orquestrar a interação com um modelo de linguagem grande (LLM) local através do Ollama (configurado por defeito para `phi3:mini`).

## Estrutura do Projeto

```
llm_fecomdb_app/
├── utils/
│   ├── __init__.py       # Torna utils um pacote Python
│   ├── llm_utils.py      # Funções para configurar Langchain e Ollama
│   └── mongo_utils.py    # Funções para conectar e interagir com MongoDB
├── .env.example          # Ficheiro de exemplo para variáveis de ambiente
├── .env                  # Ficheiro com as suas variáveis de ambiente (NÃO versionar)
├── app.py                # Ficheiro principal da aplicação Streamlit
├── requirements.txt      # Dependências Python do projeto
└── README.md             # Este ficheiro
```

## Pré-requisitos

1.  **Python 3.8+**: Certifique-se de que tem o Python instalado.
2.  **MongoDB Atlas**: Uma conta no MongoDB Atlas com a base de dados `fecomdb_data` populada com as coleções do ficheiro `fecomdb.json` (este passo já foi realizado).
3.  **Ollama**: Ollama instalado e em execução na sua máquina local. Pode descarregá-lo em [https://ollama.com/](https://ollama.com/).
4.  **Modelo Ollama**: O modelo LLM desejado descarregado através do Ollama. Por defeito, este projeto utiliza `phi3:mini`. Execute `ollama pull phi3:mini` no seu terminal se ainda não o tiver.
5.  **Git (Opcional)**: Para clonar o repositório se estiver num sistema de controlo de versões.
6.  **Ambiente Virtual (Recomendado)**: Para isolar as dependências do projeto.

## Configuração (Setup)

1.  **Clonar o Repositório (se aplicável)**:
    ```bash
    # Se recebeu os ficheiros num zip, extraia-os para uma pasta.
    # Se estiver num repo git:
    # git clone <url_do_repositorio>
    cd llm_fecomdb_app
    ```

2.  **Criar e Ativar Ambiente Virtual (Recomendado)**:
    *   **Windows (Command Prompt/PowerShell)**:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **macOS/Linux (Bash/Zsh)**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instalar Dependências**: 
    No seu terminal, com o ambiente virtual ativado, execute:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variáveis de Ambiente**:
    *   Copie o ficheiro `.env.example` para um novo ficheiro chamado `.env` na raiz do projeto (`llm_fecomdb_app/`).
    *   Edite o ficheiro `.env` e preencha os valores corretos:
        *   `MONGO_URI`: A sua connection string completa do MongoDB Atlas (a que forneceu inicialmente).
        *   `MONGO_DB_NAME`: O nome da base de dados onde os dados foram importados (deve ser `fecomdb_data`).
        *   `OLLAMA_BASE_URL`: O URL onde o Ollama está a ser executado (normalmente `http://localhost:11434` se estiver localmente).
        *   `OLLAMA_MODEL`: O nome exato do modelo Ollama que descarregou (ex: `phi3:mini`).

5.  **Verificar Ollama**: Certifique-se de que o serviço Ollama está em execução no seu sistema e que o modelo (`phi3:mini` ou outro especificado) está disponível (`ollama list`).

## Executar a Aplicação

1.  Abra o seu terminal (com o ambiente virtual ativado) na pasta raiz do projeto (`llm_fecomdb_app`).
2.  Execute o Streamlit:
    ```bash
    streamlit run app.py
    ```
3.  A aplicação deverá abrir automaticamente no seu navegador web. Se não abrir, aceda ao URL local fornecido pelo Streamlit (geralmente `http://localhost:8501`).

## Como Usar

1.  A interface da aplicação mostrará um título, uma descrição e uma caixa de texto para inserir a sua pergunta.
2.  Na barra lateral, pode ver a lista de coleções disponíveis na base de dados `fecomdb_data` para referência.
3.  Digite a sua pergunta sobre os dados económicos na caixa de texto (ex: "Quais coleções contêm dados sobre o IPCA?", "Fale-me sobre os dados de ocupação disponíveis", "Qual a estrutura dos dados na coleção pmc_8881_RNm1?").
4.  Clique no botão "Perguntar".
5.  A aplicação enviará a sua pergunta, juntamente com o contexto dos nomes das coleções, para o modelo LLM via Ollama.
6.  A resposta gerada pelo LLM será exibida abaixo.

**Nota Importante sobre as Respostas:** A configuração atual do prompt instrui o LLM a usar os nomes das coleções como contexto e a responder com base nesse contexto e no seu conhecimento geral. Ele foi instruído a **não** tentar executar consultas diretas para obter valores específicos, mas sim a descrever os dados disponíveis. Para obter valores exatos, seria necessário implementar uma lógica mais complexa (como um Agente Langchain ou RAG - Retrieval-Augmented Generation) que possa construir e executar consultas MongoDB com base na pergunta do utilizador.

## Exemplos de Perguntas

*   "Quais são as coleções disponíveis na base de dados?"
*   "Que tipo de informação posso encontrar na coleção `ipca_7060_brasil`?"
*   "Existem dados sobre desocupação? Em que coleção?"
*   "Fale sobre os dados da Pesquisa Mensal de Comércio (PMC)."
*   "Qual a diferença entre as coleções `pmc_8881_RNm1` e `pmc_8881_RNm12`?"

## Próximos Passos e Melhorias (Sugestões)

*   **Implementar RAG**: Em vez de apenas passar os nomes das coleções, recuperar documentos relevantes do MongoDB com base na pergunta do utilizador e passá-los como contexto mais específico para o LLM.
*   **Criar um Agente Langchain**: Desenvolver um agente que possa analisar a pergunta, decidir qual coleção consultar, construir a query MongoDB apropriada, executar a query e, em seguida, usar o LLM para formatar a resposta.
*   **Melhorar o Tratamento de Erros**: Adicionar mais detalhes sobre erros de conexão ou de processamento na interface do Streamlit.
*   **Interface Mais Rica**: Adicionar visualizações de dados ou a capacidade de explorar dados de coleções específicas.
*   **Seleção de Modelo/Coleção**: Permitir ao utilizador escolher o modelo Ollama ou focar a pergunta numa coleção específica através da interface.

