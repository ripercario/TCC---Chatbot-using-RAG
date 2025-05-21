from rag_pipeline import retrieve_evidence
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_model(prompt: str, model="llama3") -> str:
    payload = {
        "model": model,
        "prompt": prompt
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_response = line.decode('utf-8')
                    response_data = json.loads(json_response)
                    full_response += response_data.get("response", "")
                except ValueError as e:
                    print(f"[ERRO] Não foi possível processar o JSON: {e}")

        return full_response.strip()
    except requests.RequestException as e:
        return f"[ERRO] FALHA DE COMUNICAÇÃO COM O MODELO - {e}"

def get_model_response(prompt: str) -> str:
    # Recupera evidência do PDF
    evidence = retrieve_evidence(prompt)

    if not evidence.strip():
        return "Nenhuma evidência relevante foi encontrada no documento para responder à sua pergunta."
    
    # Monta o prompt com contexto
    full_prompt = f"""
Com base no conteúdo do documento a seguir, responda o que se pede. 
[CONTEÚDO DO DOCUMENTO]
{evidence}
[FIM DO CONTEÚDO]

PERGUNTA: {prompt}
"""
    return ask_model(full_prompt)
