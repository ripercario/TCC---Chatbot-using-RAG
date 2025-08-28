import asyncio
import json
import os
from typing import List

# Importa as ferramentas do LangChain e Pydantic para o processamento.
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


# Define o schema dos dados para a extração do grafo de conhecimento.
class Relation(BaseModel):
    """Representa uma única relação: Sujeito -> Predicado -> Objeto."""
    source: str = Field(..., description="O sujeito da relação (a entidade de origem).")
    target: str = Field(..., description="O objeto da relação (a entidade de destino).")
    label: str = Field(..., description="O predicado que descreve a conexão (a relação).")

class KnowledgeGraph(BaseModel):
    """Define a estrutura de saída para o LLM: uma lista de relações."""
    relations: List[Relation] = Field(..., description="Uma lista de todas as relações factuais extraídas.")


# Cria o parser de saída que instrui o LLM sobre o formato JSON esperado.
parser = JsonOutputParser(pydantic_object=KnowledgeGraph)

# Define o template do prompt com instruções claras para o LLM.
prompt = ChatPromptTemplate.from_messages([
    ("system", """
Você é um sistema de extração de conhecimento. Sua função é ler o texto fornecido e convertê-lo em um grafo de conhecimento estruturado no formato JSON, identificando as relações factuais entre as entidades.

Siga estas regras estritamente:
1. Analise o [TEXTO] e identifique as entidades principais (pessoas, equipamentos, processos, etc.).
2. Extraia apenas as relações diretas e factuais entre essas entidades.
3. Formate cada relação como um trio: (Entidade Fonte, Relação, Entidade Alvo).
4. Retorne TODAS as relações encontradas no formato JSON especificado. Se nenhuma for encontrada, retorne uma lista de relações vazia.
"""),
    ("human", "Aqui está o texto para análise:\n\n[TEXTO]\n{input}\n\nSiga estritamente as instruções de formato abaixo:\n{format_instructions}")
])


async def build_and_save_graph(pdf_path: str, output_filename: str = "knowledge_graph.json"):
    """
    Orquestra o processo de extração de ponta a ponta: carrega, divide,
    extrai relações de cada chunk e salva o grafo consolidado.
    """
    print(f"Iniciando a criação do grafo de conhecimento a partir de '{pdf_path}'...")

    # Carrega o documento usando Unstructured com OCR para português.
    loader = UnstructuredPDFLoader(pdf_path, strategy="ocr_only", languages=["por"])
    documents = loader.load()
    
    # Divide o documento em chunks de texto para processamento.
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    print(f"O documento foi dividido em {len(chunks)} chunks para análise.")

    # Inicializa o LLM e a cadeia de extração.
    llm = ChatOllama(model="llama3", format="json", temperature=0)
    
    # Constrói a cadeia de processamento: prompt -> llm -> parser.
    extraction_chain = prompt | llm | parser

    # Itera sobre cada chunk para extrair as relações de forma assíncrona.
    all_relations = []
    print(f"Iniciando extração de relações de {len(chunks)} chunks... (Este processo será longo)")
    
    for i, chunk in enumerate(chunks):
        print(f"Processando chunk {i + 1}/{len(chunks)}...")
        try:
            # Invoca a cadeia com o texto do chunk e as instruções de formato.
            response = await extraction_chain.ainvoke({
                "input": chunk.page_content,
                "format_instructions": parser.get_format_instructions()
            })
            
            if response and response.get('relations'):
                relations_list = response['relations']
                all_relations.extend(relations_list)
                print(f"  -> {len(relations_list)} relações encontradas.")
            else:
                print(f"  -> Nenhuma relação encontrada.")
        except Exception as e:
            print(f"  -> Erro ao processar o chunk: {e}")

    # Salva o grafo de conhecimento consolidado em um arquivo JSON.
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_relations, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Processo finalizado. {len(all_relations)} relações foram salvas em '{output_filename}'.")


if __name__ == '__main__':
    # Define o caminho para o PDF a ser processado.
    PDF_FILE_PATH = "Docmuentos/Book de Operações Ajinomoto - Inovações e Resultados 2025 (1°S) - Rev_00.pdf"
    
    if os.path.exists(PDF_FILE_PATH):
        asyncio.run(build_and_save_graph(PDF_FILE_PATH))
    else:
        print(f"ERRO: O arquivo PDF não foi encontrado no caminho especificado: {PDF_FILE_PATH}")