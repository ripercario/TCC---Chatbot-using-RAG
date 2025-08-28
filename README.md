# 🤖 Assistente Virtual com IA para Consulta de Documentos Corporativos

**📌 Status do Projeto:** Protótipo Funcional

Este repositório contém o código-fonte do projeto de Trabalho de Conclusão de Curso (TCC) em Engenharia de Computação.  
A solução consiste em um chatbot inteligente projetado para otimizar o acesso à informação em manuais e documentos operacionais complexos, utilizando uma arquitetura de RAG Híbrida.

---

## 📖 Visão Geral

Em ambientes corporativos, especialmente em setores como a logística, a informação crítica está frequentemente dispersa em extensos arquivos PDF, muitas vezes contendo diagramas, tabelas e imagens.  
Isso torna a busca por procedimentos específicos uma tarefa lenta e ineficiente.

Este projeto implementa uma solução avançada de RAG (Retrieval-Augmented Generation) que utiliza uma **busca híbrida**, combinando a precisão de um **Grafo de Conhecimento** com a flexibilidade da **busca vetorial**.  
Assim, colaboradores podem fazer perguntas em linguagem natural e receber respostas precisas, extraídas e sintetizadas diretamente dos documentos da empresa — incluindo texto dentro de imagens.

---

## ✨ Features

- 🔎 **Busca Híbrida**: Combina consultas factuais via Grafo de Conhecimento com busca semântica em índice vetorial.  
- 🧩 **Grafo de Conhecimento**: Extrai entidades e relações (ex.: nomes, cargos, especificações de equipamentos).  
- 📑 **OCR**: Extrai e indexa texto de imagens, tabelas e diagramas dentro dos PDFs.  
- ⚡ **Atualização Incremental**: Permite adicionar novos documentos sem reprocessar todos os arquivos.  
- 💬 **Interface de Chat Intuitiva**: Desenvolvida com Chainlit.  
- 🔒 **Arquitetura 100% Local**: Garantia de privacidade e segurança dos dados.  

---

## 🏗️ Arquitetura

O sistema utiliza uma **arquitetura de RAG Híbrida**, dividida em duas bases de conhecimento:

### 📊 Grafo de Conhecimento (para Fatos)
- Usa o modelo **Llama 3** com engenharia de prompt avançada para extrair relações estruturadas (ex.: `Entidade -> Relação -> Entidade`).  
- Os fatos são armazenados em `knowledge_graph.json`, ideal para consultas precisas.  

### 📚 Índice Vetorial (para Contexto)
- Usa o modelo de embedding **Snowflake Arctic** para converter chunks de texto em vetores numéricos.  
- Os vetores são armazenados em um índice **FAISS**, ideal para buscas semânticas rápidas.  

Durante a consulta, o chatbot combina evidências das duas fontes e gera a resposta final com o **Llama 3**.

---

## 🛠️ Tecnologias Utilizadas

- **🐍 Linguagem**: Python 3.11  
- **💻 Interface**: Chainlit  
- **🧠 LLM**: Llama 3 (via Ollama)  
- **🔢 Embedding**: Snowflake Arctic (`snowflake-arctic-embed-m`)  
- **📦 Índice Vetorial**: FAISS  
- **🕸️ Extração de Grafo**: LangChain + Pydantic  
- **📑 PDF e OCR**: Unstructured, Tesseract, Poppler  
- **📂 Ambiente Virtual**: venv  

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
- Python 3.11 ou superior  
- Ollama instalado e em execução  
- Tesseract OCR instalado e no PATH do sistema  
- Poppler instalado e no PATH do sistema  

### 2. Instalação
Clone o repositório e entre no diretório:

git clone https://github.com/ripercario/TCC---Chatbot-using-RAG.git
cd TCC---Chatbot-using-RAG

Crie e ative o ambiente virtual:

# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

Instale as dependências:

pip install -r requirements.txt

Baixe o modelo Llama 3 via Ollama:

ollama pull llama3

---

### 3. ⚙️ Configuração (Ingestão de Dados)

Adicione os documentos PDF na pasta `Docmuentos/`.

Crie/atualize as bases de conhecimento executando:

# Criar/atualizar índice vetorial FAISS
python create_index.py

# Criar/atualizar Grafo de Conhecimento
python app/build_graph.py

Após a execução, serão gerados:
- Pasta `data/faiss_index/`
- Arquivo `knowledge_graph.json`

---

### 4. ▶️ Execução

Com o Ollama rodando em segundo plano, inicie a aplicação:

chainlit run app/app.py -w

Acesse no navegador:  
http://localhost:8000

---

## 📁 Estrutura do Projeto

.
├── app/
│   ├── __init__.py
│   ├── app.py              # Interface com Chainlit
│   ├── build_graph.py      # Criação/atualização do Grafo de Conhecimento
│   ├── chatbot.py          # Orquestração e chamada ao modelo
│   └── rag_pipeline.py     # Criação e consulta ao índice FAISS
├── Docmuentos/             # PDFs da empresa
├── data/
│   └── faiss_index/        # Índice FAISS
├── .gitignore
├── chainlit.md
├── create_index.py         # Script de índice vetorial
├── knowledge_graph.json    # Base factual
├── README.md
└── requirements.txt

---

## ✒️ Autor

**Ricardo Percario de Souza Ribeiro**
