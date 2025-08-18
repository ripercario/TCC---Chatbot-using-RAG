from langchain_community.llms import Ollama
from rag_pipeline import retrieve_evidence

def get_model_response(prompt: str) -> str:
    """
    Orquestra o processo de RAG: recupera evidências e gera uma resposta com o LLM.
    """
    # Recupera os chunks de texto mais relevantes do vector store com base na pergunta.
    evidence = retrieve_evidence(prompt)

    # Se nenhuma evidência for encontrada, retorna uma mensagem padrão.
    if not evidence.strip():
        return "Nenhuma evidência relevante foi encontrada no documento para responder à sua pergunta."
    
    # Constrói o prompt final, inserindo as evidências recuperadas como contexto para o LLM.
    full_prompt = f"""
Com base no conteúdo do documento a seguir, responda o que se pede de forma concisa e direta. 
[CONTEÚDO DO DOCUMENTO]
{evidence}
[FIM DO CONTEÚDO]

PERGUNTA: {prompt}
"""
    
    # Tenta se comunicar com o modelo e obter uma resposta.
    try:
        # Inicializa o LLM via LangChain, apontando para o modelo 'llama3' no Ollama.
        llm = Ollama(model="llama3")
        
        # Envia o prompt completo para o LLM e aguarda a resposta.
        response = llm.invoke(full_prompt)
        
        return response.strip()
    
    except Exception as e:
        # Em caso de falha (ex: serviço do Ollama offline), retorna uma mensagem de erro.
        return f"[ERRO] FALHA DE COMUNICAÇÃO COM O MODELO - {e}"