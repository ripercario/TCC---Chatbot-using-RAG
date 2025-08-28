from app.rag_pipeline import update_or_create_vector_store

# Defina o caminho para o PDF que você quer adicionar
pdf_para_adicionar = ""

update_or_create_vector_store(pdf_para_adicionar)

print(f"Processo concluído. O documento '{pdf_para_adicionar}' foi adicionado à base de conhecimento.")