from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv()

def verificar_integridad(chunks, corpus_original):
    #Recorro todos los chunk con su indice (i), quitamos/saltos de linea
    #guardo lista de posiciones de cualqier fragmanto de que haya quedado en blanco
    vacios = [i for i, c in enumerate(chunks) if not c.page_content.strip()]

    #extraigo texto plano de cad objeto
    textos = [c.page_content for c in chunks]

    #set/conjunto es una lista de valores unicos
    hay_duplicados = len(textos) != len(set(textos))

    if vacios:
        raise ValueError(f"Se detectaron chunks vacíos en los índices: {vacios}")
    if hay_duplicados:
        print("Advertencia: Se detectaron chunks duplicados en el corpus.")

#sumar el total de caracteres de todos los chunk generados VS el total de caracteres del corpus original
    total_chars_chunks = sum(len(c.page_content) for c in chunks)
    total_chars_corpus = sum(len(d) for d in corpus_original)
    print(f"Integridad OK | Chunks: {len(chunks)} | Caracteres (corpus/chunks): {total_chars_corpus}/{total_chars_chunks}")


"""
Recibir un corpus/texto dividirlo, calcular embedding, y guardar el corpues en el vector store
"""

def indexar_corpus(corpus, persist_directory, chunk_size=200, chunk_overlap=30, es_documento=False):
#dividir en fragmantos mas pequeños corpus/texto
    splitter = RecursiveCharacterTextSplitter (
        chunk_size=chunk_size,
        chunk_overlap= chunk_overlap
    )
    #divicion en chunk
    #chunk = splitter.create_documents(text=corpus, metadatas=[{"origen:"manual.pdf", "pagina": 2}])
    chunk = splitter.create_documents(corpus) #create_documents permite agregar metadatos
    if not es_documento:
        chunk = splitter.create_documents(corpus)
    else:
        chunk = splitter.split_documents(corpus)


    verificar_integridad(chunk,corpus)

    #embedding
    embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    vector_store = Chroma.from_documents(
        documents=chunk,
        embedding=embedding,
        persist_directory=persist_directory
    )
    return vector_store

"""
funcion que abre/carga la carpeta existente del disco para leerla. No gasto tokens
"""
def cargar_vectorstore(persist_directory):
    embedding=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return Chroma(persist_directory=persist_directory, embedding_function=embedding)

def eliminar_por_ids(vectorstore, id_a_borrar):
    vectorstore.delete(ids=id_a_borrar)

def agregar_documentos(vectorstore, nuevos_textos, prefijo_id, chunk_size=200, chunk_overlap=30):

    spitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nuevo_chunk = spitter.create_documents(nuevos_textos) #lista los fragmentos

    #crear los ID
    ids_nuevos = [f"{prefijo_id}_{i}" for i in range(len(nuevo_chunk))] #["doc_0", "doc_1", "doc_2"]
    #ids_nuevos = []
    #for i in range(len(nuevos_chunk)):
    #   ids_nuevos.append(f"{prefijo_idx}_{i}"")

    #verificar_integridad(nuevo_chunk, nuevos_textos)

    try:
        vectorstore.add_documents(nuevo_chunk, ids_nuevos)
        print(f"agregados {len(nuevo_chunk)} chunk con prefijo {prefijo_id}")
    except Exception as error:
        print("error al agregar nuevos documentos", error)

#realiza ka busca semantica 
def buscar_similares(vectorstore, pregunta, k=3):
    #El modelo (Gemini) se encarga únicamente de hacer la traducción de la pregunta a vectores numéricos (gasta tokens)
    #Chroma se encarga de regresarme la lista con los chunks más parecidos
    #Chroma mide la distancia Euclidiana (L2). Entre más bajo sea el número, más cercano es el significado.
    resultados = vectorstore.similarity_search_with_score( #with_score regresa también la distancia euclidiana
        query=pregunta, #Gastamos tokens en traducir la pregunta a vectores numéricos
        k=k #La cantidad de chunks que quiero que regrese
    )

    #resultados = [ {"page_content": "CONTENIDO DEL CHUNK", "metadata": {"fuente": "documento.pdf"}}, {}, {} ]

    #iterar para imprimir todos los resultados
    for i, (doc, score)in enumerate(resultados, start=1):
        print(f"[Resultado {i}] Distancia (score): {score:.4f}")
        print(f"Contenido: {doc.page_content}")
        if doc.metadata:
            print(f"Metadata: {doc.metadata}")

    return resultados

def formatear_contexto(chunks_recuperados):
    lineas = []
    citas = {}

   
    for i, doc in enumerate(chunks_recuperados, start=1):
        #Si el chunk no se indexó con metadata["fuente"], devolverá "desconocida"
        fuente = doc.metadata.get("fuente", "desconocida")
        lineas.append(f"[{i}] {doc.page_content}")
        citas[i] = fuente

    contexto = "\n\n".join(lineas)
    return contexto, citas

def inspeccionar_chunk(vectorstore):
    datos = vectorstore.get() 
    #datos["ids"], datos ["Documents"], datos["Metadata"]
    total = len(datos["ids"])
    print(f"-- INVENTARIO de chunk en chroma (Total_{total})--")

    for i, (chunk_id, texto, meta) in enumerate(zip(datos["ids"], datos["documents"], datos["metadatas"]), start=1):
        print(f"[{i}] ID: {chunk_id}")
        print(f"Fuente/Meta: {meta}")
        resumen = texto.replace("\n","")[:100] #quita los saltos de linea y obten los primeros 100 caracteres
        print(f"contenido: {resumen}...")

if __name__=="__main__":
    CARPETA_DB = "vector_ejemplo"
#     corpus = [
#     "El cliente reintenta hasta 3 veces ante un TimeoutError, con espera creciente.",
#     "Los errores de autenticacion nunca se reintentan: fallan de inmediato con un "
#     "ValueError.",
#     "El costo de cada llamada se calcula a partir de totalTokenCount y la tarifa "
# ]
#     #indexar_corpus(corpus, CARPETA_DB) #almacena el texto
#     #indexar_corpus(corpus=corpus, persist_directory=CARPETA_DB, chunk_size=250, chunk_overlap=35)

    vs = cargar_vectorstore(CARPETA_DB) #carga la carpeta para poder consultar/actualizar mas adelante
#     print ("chunk indexados:", vs._collection.count())#imprime los chunk indexados

#     datos = vs.get()
#     print ("IDs almacenados:", datos["ids"])
#     print ("Chunks almacenados:", datos["documents"])

# eliminar por id
#  eliminar_por_ids(
#          vectorstore=vs,
#          id_a_borrar=["9a08cd6c-401a-4999-85a4-0354c4a0051a"],
#      )
# print("IDs después de borrar:", vs.get()["ids"])


# nueva_politica = ["Los envios internacionales tienen un tiempo estimado de entrega de 20 a 30 dias habiles."]
#     #agregar_documentos(vs, nueva_politica, "doc_nuevo", 150, 20)
# agregar_documentos(
#         vectorstore=vs, 
#         nuevos_textos=nueva_politica, 
#         prefijo_id="doc_nuevo", 
#         chunk_size=150, 
#         chunk_overlap=20
#     )

# datos = vs.get()
# print("IDs almacenados: ", datos["ids"])
# print("Chunks almacenados: ", datos["documents"])

#     vs = cargar_vectorstore(CARPETA_DB)
#     pregunta = "¿Qué hace el sistema cuando hay un fallo de red o tiempo de espera?"
    
#     chunks_recuperados = buscar_similares(vs, pregunta, k=2)


# #k = Cantidad de chunks que quiero que regrese
#     retrievier = vs.as_retriever(search_kwargs={"k": 2}) #Adapta lo que tenía en Chroma para poder utilizarlo en LangChain
#     #Ventaja principal: Cadena o Agente | 
#     resultados = retrievier.invoke("¿Cuánto tarda un envío en el mismo país?")
#     for r in resultados:
#         print(r.page_content)


 #Instalación adicional si queremos leer pdf, docs, etc
    with open("manual_de_usuario.txt", "r", encoding="utf-8") as f: #r: read, a: append, w: write
        contenido = f.read()

    documentos = [Document(page_content=contenido, metadata={"fuente": "manual_de_usuario.txt", "fecha": "2026-11-13"})]

    #indexar_corpus(documentos, CARPETA_DB, es_documento=True) #comentado para que no vuelvan a ingresar el manual de usuario en su vs

    datos = vs.get()
    print("IDs almacenados: ", datos["ids"])
    print("Chunks almacenados: ", datos["documents"])


    retriever = vs.as_retriever(search_kwargs={"k":3})
    chunk_recuperados = retriever.invoke("¿Cuantos reintentos tengo ante un error")

    contexto, citas = formatear_contexto(chunk_recuperados)
    print("--CONTEXTO FORMATEADO--")
    print(contexto)
    print("--DICCCIONARIO DE CITAS--")
    print(citas)

    inspeccionar_chunk(vs)


#codigo para borrar todo mi vector store
    # if os.path.exists(CARPETA_DB):
    #     shutil.rmtree(CARPETA_DB)