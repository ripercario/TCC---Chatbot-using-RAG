# Assistente Virtual com IA para Consulta de Documentos Corporativos

**Status do Projeto: Em Desenvolvimento (Protótipo Funcional)**

Este repositório contém o código-fonte do projeto de Trabalho de Conclusão de Curso (TCC) em Engenharia de Computação, que consiste em um chatbot inteligente projetado para otimizar o acesso à informação em manuais e documentos operacionais de uma empresa.

## 📖 Visão Geral

Em ambientes corporativos, especialmente em setores como a logística, a informação crítica está frequentemente dispersa em extensos arquivos PDF. Isso torna a busca por procedimentos específicos uma tarefa lenta e ineficiente.

Este projeto implementa uma solução baseada em **RAG (Retrieval-Augmented Generation)** que permite aos colaboradores fazerem perguntas em linguagem natural e receberem respostas precisas e contextuais, extraídas diretamente dos documentos da empresa.

## 🏗️ Arquitetura

O sistema é dividido em três camadas lógicas, conforme o diagrama do projeto:

1.  **Interface:** Construída com **Chainlit**, é a camada de apresentação responsável pelo fluxo de interação com o usuário:
    * `Campo para entrada de pergunta` -> `Envio do prompt ao backend` -> `Recuperação de resposta` -> `Exibição da resposta do chatbot`.

2.  **Backend:** Onde os processos são orquestrados. Esta camada implementa a lógica da consulta e o pipeline de dados:
    * **Geração de Vetores:** Converte os `chunks` dos documentos em `embeddings` e os armazena em um índice vetorial com **FAISS**.
    * **Lógica de Consulta:** Recebe a pergunta, busca por `chunks` relevantes no índice FAISS, monta um prompt final com o contexto recuperado e o envia para o modelo Llama 3 para a geração da resposta.

3.  **Chatbot:** Contém os componentes de Inteligência Artificial que são a base da solução:
    * **Modelo (LLM):** `Llama 3`, responsável por entender a pergunta e gerar a resposta final.
    * **Embedding:** `sentence-transformers/all-MiniLM-L6-v2`, responsável por converter os trechos de texto dos PDFs em vetores numéricos.
    * **RAG (Retrieval-Augmented Generation):** A técnica que aumenta a capacidade do LLM com informações de documentos externos, garantindo respostas baseadas nos manuais da empresa.

## 🛠️ Tecnologias Utilizadas

-   **Linguagem:** Python 3.10+
-   **Interface:** Chainlit
-   **Modelo de Linguagem (LLM):** Llama 3 (via Ollama)
-   **Modelo de Embedding:** `sentence-transformers/all-MiniLM-L6-v2`
-   **Índice Vetorial:** FAISS
-   **Manipulação de PDF:** PyPDFLoader
-   **Ambiente Virtual:** venv

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

### 1. Pré-requisitos

-   Python 3.10 ou superior
-   [Ollama](https://ollama.com/) instalado e em execução.

### 2. Instalação

**a. Clone o repositório:**
```bash
git clone [https://github.com/ripercario/TCC---Chatbot-using-RAG.git](https://github.com/ripercario/TCC---Chatbot-using-RAG.git)
cd seu-repositorio
```

**b. Crie e ative um ambiente virtual:**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

**c. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**d. Baixe o modelo Llama 3 via Ollama:**
```bash
ollama pull llama3
```

### 3. Configuração

**a. Adicione os seus documentos:**
Coloque todos os manuais e documentos em formato `.pdf` dentro da pasta `/data`.

**b. Crie o índice vetorial:**
Execute o script `create_index.py` para processar os PDFs e criar o banco de dados vetorial FAISS. Isso precisa ser feito apenas uma vez ou sempre que os documentos na pasta `/data` forem alterados.
```bash
python create_index.py
```
Ao final do processo, uma nova pasta chamada `data/faiss_index` será criada.

### 4. Execução

Com o Ollama em execução em segundo plano, inicie a aplicação Chainlit:
```bash
chainlit run app/app.py -w
```
A flag `-w` (watch) reinicia o servidor automaticamente sempre que você salvar uma alteração no código.

Abra o seu navegador e acesse `http://localhost:8000` para começar a interagir com o chatbot.

## 📁 Estrutura do Projeto
```
.
├── app/
│   ├── __init__.py
│   ├── app.py          # Lógica da interface com Chainlit
│   ├── chatbot.py      # Lógica de orquestração e chamada ao modelo
│   └── rag_pipeline.py # Funções de criação e consulta do índice RAG
├── data/
│   ├── exemplo.pdf     # Coloque seus PDFs aqui
│   └── faiss_index/    # Criado após a execução de create_index.py
├── .gitignore
├── chainlit.md
├── create_index.py     # Script para criar o índice vetorial
├── main.py             # Ponto de entrada para testes via terminal
├── README.md
└── requirements.txt
```

## ✒️ Autor

-   **Ricardo Percario de Souza Ribeiro** 