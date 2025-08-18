# app/rag_pipeline.py

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# Define o caminho padrão para o índice FAISS salvo.
INDEX_PATH = "data/faiss_index"

# Classe customizada para o embedding do Snowflake Arctic que aplica o prefixo 'query:'.
class ArcticHuggingFaceEmbeddings(HuggingFaceEmbeddings):
    """
    Classe de embedding customizada para os modelos Snowflake Arctic.
    Adiciona o prefixo 'query: ' às perguntas para otimizar a busca,
    conforme a recomendação do modelo.
    """
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # Documentos não recebem prefixo no modelo Arctic.
        return super().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        # Adiciona o prefixo 'query:' para otimizar a busca por similaridade.
        prefixed_text = f"query: {text}"
        return super().embed_query(prefixed_text)


def update_or_create_vector_store(pdf_path: str, index_path: str = INDEX_PATH):
    """
    Processa um arquivo PDF e cria ou atualiza um vector store local.
    Se um índice já existe no `index_path`, os novos documentos são adicionados a ele.
    Caso contrário, um novo índice é criado.
    """
    print(f"Processando documento: {pdf_path}...")
    try:
        # Carrega o documento usando Unstructured com OCR forçado para português.
        loader = UnstructuredPDFLoader(pdf_path, strategy="ocr_only", languages=["por"])
        new_documents = loader.load()
        
        # Divide os documentos carregados em chunks de texto.
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        new_chunks = splitter.split_documents(new_documents)
        
        # Inicializa o modelo de embedding customizado.
        embeddings = ArcticHuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m")

    except Exception as e:
        print(f"Erro ao processar o documento {pdf_path}: {e}")
        return

    # Verifica se o índice local já existe para decidir entre atualizar ou criar.
    if os.path.exists(index_path):
        print(f"Índice existente encontrado. Atualizando...")
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        vectorstore.add_documents(new_chunks)
        print("Índice atualizado.")
    else:
        print(f"Nenhum índice encontrado. Criando novo índice...")
        os.makedirs(index_path, exist_ok=True)
        vectorstore = FAISS.from_documents(new_chunks, embeddings)
        print("Novo índice criado.")

    # Salva o estado do vector store no disco.
    vectorstore.save_local(index_path)
    print(f"Índice salvo com sucesso em '{index_path}'.")

def load_vector_store(index_path: str = INDEX_PATH):
    """Carrega o índice FAISS do disco."""
    if not os.path.exists(index_path):
        print(f"Erro: Índice não encontrado em '{index_path}'.")
        return None
    
    embeddings = ArcticHuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m")
    
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)


def retrieve_evidence(query: str, k: int = 15):
    """
    Recupera os 'k' chunks de texto mais relevantes para uma dada query.
    """
    vectorstore = load_vector_store()
    if vectorstore is None:
        return "A base de conhecimento está vazia. Por favor, adicione um PDF."

    # Realiza a busca por similaridade no vector store.
    results = vectorstore.similarity_search(query, k=k)
    
    # Formata os resultados como uma única string de contexto.
    evidence = "\n---\n".join([doc.page_content for doc in results])
    
    # Imprime as evidências recuperadas para fins de depuração.
    print("\n--- EVIDÊNCIAS RECUPERADAS PARA O LLM ---\n")
    print(evidence)
    
    return evidence