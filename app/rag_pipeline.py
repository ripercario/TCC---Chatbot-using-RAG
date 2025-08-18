# app/rag_pipeline.py

# --- MUDANÇA: O Loader foi trocado para UnstructuredPDFLoader ---
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# O caminho do índice continua o mesmo
INDEX_PATH = "data/faiss_index"

# Classe customizada para o modelo Snowflake Arctic
class ArcticHuggingFaceEmbeddings(HuggingFaceEmbeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # Para o Arctic, os documentos não levam prefixo.
        return super().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        # Adiciona o prefixo "query:" apenas para a pergunta do usuário.
        prefixed_text = f"query: {text}"
        return super().embed_query(prefixed_text)


def update_or_create_vector_store(pdf_path: str, index_path: str = INDEX_PATH):
    """
    Verifica se um vector store já existe.
    - Se existir, carrega-o e adiciona o novo documento.
    - Se não existir, cria um novo a partir do documento.
    """
    print(f"Processando o novo documento com Unstructured (Estratégia OCR): {pdf_path}...")
    try:
        # --- MUDANÇA PRINCIPAL: Forçando a estratégia de OCR ---
        # Isso garante que o Tesseract será usado em todas as páginas.
        loader = UnstructuredPDFLoader(pdf_path, strategy="ocr_only", languages=["por"])
        
        new_documents = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        new_chunks = splitter.split_documents(new_documents)
        
        embeddings = ArcticHuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m")

    except Exception as e:
        print(f"Erro ao processar o novo documento {pdf_path}: {e}")
        return

    if os.path.exists(index_path):
        print(f"Índice existente encontrado em '{index_path}'. Atualizando...")
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        vectorstore.add_documents(new_chunks)
        print("Novos documentos adicionados ao índice.")
    else:
        print(f"Nenhum índice encontrado. Criando um novo em '{index_path}'...")
        os.makedirs(index_path, exist_ok=True)
        vectorstore = FAISS.from_documents(new_chunks, embeddings)
        print("Novo índice criado.")

    vectorstore.save_local(index_path)
    print(f"Índice salvo com sucesso em '{index_path}'.")

def load_vector_store(index_path: str = INDEX_PATH):
    if not os.path.exists(index_path):
        print("Erro: Nenhum índice encontrado para carregar. Por favor, adicione um documento primeiro.")
        return None
    
    embeddings = ArcticHuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-m")
    
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)


def retrieve_evidence(query: str, k: int = 15):
    vectorstore = load_vector_store()
    if vectorstore is None:
        return "A base de conhecimento está vazia. Por favor, adicione um P" \
        "DF."

    results = vectorstore.similarity_search(query, k=k)
    evidencias = "\n---\n".join([doc.page_content for doc in results])

    # --- ADICIONE ESTAS DUAS LINHAS PARA DEPURAÇÃO ---
    print("\n--- EVIDÊNCIAS RECUPERADAS PARA O LLM ---\n")
    # --- FIM DA ADIÇÃO ---

    return evidencias