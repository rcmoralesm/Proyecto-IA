from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

texto=(
"""
Archivo de prueba: un archivo llamado "test_chunking.py" en tu entorno de desarrollo, 
donde vas a pegar los bloques de código de esta lección uno debajo del otro, en el orden 
en que aparecen. Todo el código forma parte de un mismo script continuo: el segundo bloque 
reutiliza la variable "texto" definida en el primero, y el cuarto la reutiliza otra vez, así que 
no los ejecutes por separado en terminales independientes. Al terminar, ejecuta el archivo completo 
con "python test_chunking.py".
"""
)

#chuking tamaño fijo
# splitter_fijo = CharacterTextSplitter(separator="", chunk_size=110, chunk_overlap=0)
# chunks_fijo =splitter_fijo.split_text(texto)

# for i, chunk in enumerate(chunks_fijo):
#     print(f"*** Chunk {i} ({len(chunk)} caracteres) ***")
#     print (chunk)

    #chuking recursivo
splitter_recursivo = RecursiveCharacterTextSplitter (chunk_size=110, chunk_overlap=20)
chunk_recursivo= splitter_recursivo.split_text(texto)

for i, chunk in enumerate(chunk_recursivo):
    print(f"*** Chunk {i} ({len(chunk)} caracteres) ***")
    print (chunk_recursivo)