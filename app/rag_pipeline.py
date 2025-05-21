from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

INDEX_PATH = "data/faiss_index"

def create_vector_store(pdf_path: str, index_path: str = INDEX_PATH):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()



    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)


    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = FAISS.from_documents(chunks, embeddings)
    os.makedirs(index_path, exist_ok=True)
    vectorstore.save_local(index_path)

def load_vector_store(index_path: str = INDEX_PATH):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

def retrieve_evidence(query: str, k: int = 8):

    vectorstore = load_vector_store()
    results = vectorstore.similarity_search(query, k=k)
    evidencias = "\n---\n".join([doc.page_content for doc in results])

    return evidencias