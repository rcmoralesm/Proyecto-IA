from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_chroma import Chroma

load_dotenv()

#creamos el vector
embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

try:
    vector = embedding.embed_query("Hola, como estas?")
    vector2 = embedding.embed_query("que tal, como va todo?")
except Exception as error:
    mensaje = str(error)
    if "429" in mensaje or "RESOURCE_EXHAUSTED" in mensaje:
        print ("limite de peticiones alcanzado")
    else:
        print("no se pudo generar embedding")

#imprimimos el embedding dtraducido del vector

print ("dimension:", len(vector))
print ("Primeros valores", vector[:5])
print ("*****")
print ("Dimension:", len(vector2))
print ("Primeros valores", vector2[:5])

#creando base de datos vector
vector_store= Chroma(
    collection_name="ejemplo_rag",
    embedding_function=embedding,
    persist_directory="./chroma_db"
)

#agrega un fragmento del texto chunk al vector
#vector_store.add_texts(["El cliente realiza hasta 3 reintentos en caso de error de red"])

datos=vector_store.get() #obtengo la coleccion completa
print("Id almacenados:", datos["ids"])
print("textos guardados:", datos["documents"])

#consulta base de datos
consulta = "¿Que ocurre si falla?"
documentos_recuperados = vector_store.similarity_search(consulta, k=2)# que responda con 2 documentos

for doc in documentos_recuperados:
    print("contenidos encontrados: ", doc.page_content)