# Assistente Virtual com IA para Consulta de Documentos Corporativos

**Status do Projeto: Em Desenvolvimento (Protótipo Funcional)**

Este repositório contém o código-fonte do projeto de Trabalho de Conclusão de Curso (TCC) em Engenharia de Computação, que consiste em um chatbot inteligente projetado para otimizar o acesso à informação em manuais e documentos operacionais de uma empresa.

## 📖 Visão Geral

Em ambientes corporativos, especialmente em setores como a logística, a informação crítica está frequentemente dispersa em extensos arquivos PDF, muitas vezes contendo diagramas, tabelas e imagens. Isso torna a busca por procedimentos específicos uma tarefa lenta e ineficiente.

Este projeto implementa uma solução avançada de **RAG (Retrieval-Augmented Generation)** que permite aos colaboradores fazerem perguntas em linguagem natural e receberem respostas precisas e contextuais, extraídas diretamente dos documentos da empresa, incluindo texto dentro de imagens.

## ✨ Features

* **Busca Semântica:** Entende o significado da pergunta, não apenas as palavras-chave.
* **OCR (Reconhecimento Óptico de Caracteres):** Capaz de extrair e indexar texto de imagens e diagramas dentro dos PDFs.
* **Atualização Incremental:** Permite adicionar novos documentos à base de conhecimento sem a necessidade de reprocessar todos os arquivos existentes.
* **Interface de Chat Intuitiva:** Utiliza Chainlit para uma experiência de usuário moderna e interativa.
* **Arquitetura 100% Local:** Roda inteiramente na máquina do usuário, garantindo a privacidade e a segurança dos dados.

## 🏗️ Arquitetura

O sistema é dividido em três camadas lógicas principais:

1.  **Interface (Frontend):** Construída com **Chainlit**, é a camada de apresentação responsável pelo fluxo de interação com o usuário.
2.  **Lógica da Aplicação (Backend):** Orquestra os processos, conectando a interface à pipeline de IA.
    * Recebe a pergunta do usuário via `app.py`.
    * Utiliza o `chatbot.py` para coordenar a busca e a geração da resposta.

3.  **Pipeline de Dados e IA (RAG Core):** Contém os componentes de Inteligência Artificial que são a base da solução.
    * **Ingestão de Documentos:** Utiliza `Unstructured` com **Tesseract** e **Poppler** para um processamento robusto de PDFs, extraindo texto de forma eficaz, inclusive de imagens (OCR).
    * **Modelo de Embedding:** Usa o **Snowflake Arctic (`snowflake-arctic-embed-m`)** para converter os trechos de texto em vetores numéricos de alta qualidade.
    * **Índice Vetorial:** Armazena os vetores em um índice **FAISS** local para buscas rápidas por similaridade.
    * **Modelo de Linguagem (LLM):** O **Llama 3**, rodando via **Ollama**, recebe o contexto recuperado pelo FAISS e gera a resposta final em linguagem natural.

## 🛠️ Tecnologias Utilizadas

-   **Linguagem:** Python 3.11 (recomendado para maior compatibilidade)
-   **Interface:** Chainlit
-   **Modelo de Linguagem (LLM):** Llama 3 (via Ollama)
-   **Modelo de Embedding:** Snowflake Arctic (`snowflake-arctic-embed-m`)
-   **Índice Vetorial:** FAISS
-   **Manipulação de PDF e OCR:** Unstructured, Tesseract, Poppler
-   **Ambiente Virtual:** venv

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

### 1. Pré-requisitos

-   Python 3.11 ou superior
-   [Ollama](https://ollama.com/) instalado e em execução.
-   **Tesseract OCR:** Instalado e com seu caminho adicionado à variável de ambiente `PATH` do sistema.
-   **Poppler:** Utilitários baixados e com a pasta `bin` adicionada à variável de ambiente `PATH` do sistema.

### 2. Instalação

**a. Clone o repositório:**
```bash
git clone [https://github.com/ripercario/TCC---Chatbot-using-RAG.git](https://github.com/ripercario/TCC---Chatbot-using-RAG.git)
cd TCC---Chatbot-using-RAG
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
Coloque todos os manuais e documentos em formato `.pdf` em um caminho, que será passado para o `create_index.py`.

**b. Crie o índice vetorial:**
Execute o script `create_index.py` para processar os PDFs e criar o banco de dados vetorial FAISS.
python create_index.py
```

Observação: Este processo pode ser lento na primeira vez devido ao OCR. Ele só precisa ser executado quando novos documentos são adicionados.

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
│   └── faiss_index/    # Criado/atualizado após a execução de create_index.py
├── .gitignore
├── chainlit.md
├── create_index.py     # Script para criar/atualizar o índice vetorial
├── README.md
└── requirements.txt
```

## ✒️ Autor

-   **Ricardo Percario de Souza Ribeiro** 