import json
import os

# Importa as ferramentas necessárias do projeto.
from langchain_community.llms import Ollama
from rag_pipeline import retrieve_evidence

# --- Carregamento e Busca no Grafo de Conhecimento ---

KNOWLEDGE_GRAPH_PATH = "knowledge_graph.json"

def load_knowledge_graph():
    """Carrega o grafo de conhecimento do arquivo JSON, se ele existir."""
    if os.path.exists(KNOWLEDGE_GRAPH_PATH):
        with open(KNOWLEDGE_GRAPH_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def search_knowledge_graph(query: str, graph: list) -> str:
    """
    Realiza uma busca por palavras-chave no grafo de conhecimento.
    Retorna uma string formatada com as relações encontradas.
    """
    if not graph:
        return "Grafo de conhecimento não disponível."
        
    keywords = query.lower().split()
    found_relations = []
    for rel in graph:
        # Garante que os valores são strings antes de usar .lower().
        source_text = (rel.get('source', '') or '').lower()
        target_text = (rel.get('target', '') or '').lower()
        
        if any(keyword in source_text or keyword in target_text for keyword in keywords):
            # Garante que a relação está completa antes de ser adicionada.
            if rel.get('source') and rel.get('target') and rel.get('label'):
                found_relations.append(f"- {rel['source']} {rel['label']} {rel['target']}.")
    
    if found_relations:
        return "\n".join(found_relations)
    return "Nenhum fato direto encontrado no grafo de conhecimento."

# Carrega o grafo em memória uma vez quando o aplicativo inicia.
knowledge_graph = load_knowledge_graph()
if knowledge_graph:
    print(f"Grafo de conhecimento carregado com {len(knowledge_graph)} relações.")
else:
    print("AVISO: Arquivo 'knowledge_graph.json' não encontrado. A busca no grafo não funcionará.")


# --- Engenharia de Prompt e Orquestração da Resposta ---

SYSTEM_PROMPT = """
## PERSONA
Você é um assistente de IA especialista, consultando o "Book de Operações Ajinomoto". Sua função é fornecer respostas precisas e factuais.

## TAREFA
Sua tarefa é responder à [PERGUNTA DO USUÁRIO] utilizando duas fontes de informação:
1.  **[FATOS DIRETOS DO GRAFO]:** Uma lista de fatos estruturados e precisos.
2.  **[CONTEXTO DO DOCUMENTO]:** Trechos de texto mais longos para contexto geral.

## REGRAS
1.  Priorize os [FATOS DIRETOS DO GRAFO] para responder a perguntas sobre dados específicos (números, nomes, cargos, etc.).
2.  Use o [CONTEXTO DO DOCUMENTO] para responder a perguntas mais abertas sobre processos e descrições.
3.  Baseie sua resposta **ESTRITAMENTE** nas informações fornecidas. Não invente nada.
4.  Se a informação não for encontrada em nenhuma das fontes, responda: "A informação não foi encontrada no documento."
5.  Seja conciso e direto.
"""

def get_model_response(prompt: str) -> str:
    """
    Orquestra o processo de RAG HÍBRIDO: recupera evidências do grafo e do
    vector store (FAISS), e então gera uma resposta com o LLM.
    """
    # Realiza a busca híbrida nas duas fontes de conhecimento.
    print("\nBuscando fatos no Grafo de Conhecimento...")
    graph_evidence = search_knowledge_graph(prompt, knowledge_graph)
    
    print("Buscando contexto no Vector Store (FAISS)...")
    vector_evidence = retrieve_evidence(prompt)

    # Monta o prompt final com o contexto enriquecido para o LLM.
    full_prompt = f"""
{SYSTEM_PROMPT}

## EVIDÊNCIAS

### [FATOS DIRETOS DO GRAFO]
{graph_evidence}

### [CONTEXTO DO DOCUMENTO]
{vector_evidence}

## PERGUNTA DO USUÁRIO
{prompt}

## RESPOSTA FINAL:
"""
    
    # Envia o prompt para o modelo e retorna a resposta.
    try:
        llm = Ollama(model="llama3")
        response = llm.invoke(full_prompt)
        return response.strip()
    
    except Exception as e:
        return f"[ERRO] FALHA DE COMUNICAÇÃO COM O MODELO - {e}"