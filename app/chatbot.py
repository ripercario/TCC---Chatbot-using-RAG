# ADICIONADO: importação da classe Ollama do LangChain
from langchain_community.llms import Ollama
from rag_pipeline import retrieve_evidence

# REMOVIDO: A função ask_model inteira que usava 'requests' e 'json' foi removida,
# pois a classe Ollama do LangChain cuidará dessa comunicação.

def get_model_response(prompt: str) -> str:
    """
    Orquestra o processo de RAG: recupera evidências e gera uma resposta com o LLM.
    """
    # Passo 1: Recuperar evidência do PDF (nenhuma mudança aqui)
    evidence = retrieve_evidence(prompt)

    if not evidence.strip():
        return "Nenhuma evidência relevante foi encontrada no documento para responder à sua pergunta."
    
    # Passo 2: Montar o prompt com o contexto para o LLM (nenhuma mudança aqui)
    full_prompt = f"""
Com base no conteúdo do documento a seguir, responda o que se pede de forma concisa e direta. 
[CONTEÚDO DO DOCUMENTO]
{evidence}
[FIM DO CONTEÚDO]

PERGUNTA: {prompt}
"""
    
    # Passo 3: Chamar o modelo usando a integração do LangChain
    try:
        # MUDANÇA: Instanciamos o modelo Ollama diretamente
        llm = Ollama(model="llama3")
        
        # MUDANÇA: Invocamos o modelo com o prompt. O LangChain gerencia a chamada à API.
        response = llm.invoke(full_prompt)
        
        return response.strip()
    
    except Exception as e:
        # Captura exceções de comunicação, como o serviço do Ollama estar offline
        return f"[ERRO] FALHA DE COMUNICAÇÃO COM O MODELO - {e}"