from chatbot import get_model_response

while True:
    prompt = input("Faça uma pergunta ao modelo [digite 'exit' para sair]: ")
    if prompt.lower() in "exit":
        break

    answ = get_model_response(prompt)
    print("Modelo: ", answ)