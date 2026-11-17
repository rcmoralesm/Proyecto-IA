from rag_indexer import cargar_vectorstore

def precision_at_k(ids_recuperados: list[str], ids_relevantes : set[str])-> float:

    """
    ids_recuperados los que trajo el retreiver
    De los 'k' chunk que me trajo en retriever, ¿que fraccion realmente sirve?
    Devuelve 0.0 si el retreiver no devolvio ningun id
    """

    if not ids_recuperados:
        return  0.0
    #recorro los ID y si uno es relevante lo devuelvo acertado
    acertados = [i for i in ids_recuperados if i in ids_relevantes] 

    return len(acertados)/len(ids_recuperados)

def recall_at_k(ids_recuperados: list[str], ids_relecantes: set[str]) -> float | None:
    """
    Exhautividades
    De todos los chunk relevantes que existen en mi corpues, ¿Que fraccion logre rescatar?
    Devuelve none si la pregunra tiene respuesta en corpues (id_ relevantes es vacio)
    """

    if not ids_relevantes:
        return None

    acertados = [i for i in ids_recuperados if i in ids_relevantes]
    return len(acertados)/len(ids_relevantes)

def f1_score(presicion: float, recall: float | None) -> float:
    """
    Media armonica entre precision y exhautividad: equilibrio entre ambos para comparar configuraciones distintas
    de k o chunk:_size
    """
    if recall is None or (precision + recall)==0:
        return 0.0
    
    return 2 * precision * recall/(precision + recall)

def evaluar_recuperacion(retriever, casos: list[dict], k: int = 3):
    """
    Correr cada caso del conjunto de evaluaciones contra el retriever real de chroma y va a calcular precision, recall t f1
    """
    resultados = []
    for caso in casos:

        #1 cpmsultamos al retriever, cuales son los chunk que me regresa la invocaccion. si gasta tokens
        chunk = retriever.invoke(caso["pregunta"])

        #2 extraer ID
        ids_recuperados = [c.id for c in chunk]

        #3 calculamos las metricas
        p = precision_at_k(ids_recuperados, caso["id_relevantes"])
        r = recall_at_k(ids_recuperados, caso ["id_relevantes"])
        f1 = f1_score(p,r)

        #4 agregar esas metricas al resultado
        resultados.append({
            "pregunta": caso["pregunta"],
            "ids_recuperados": ids_recuperados,
            "presicion": p,
            "recall": r,
            "f1":f1
        })

if __name__ == "__main__":

    CARPETA_DB = "vectorstore_ejemplo"
    K = 3
    vs = cargar_vectorstore(CARPETA_DB)

    pregunta = "¿Cuales son los errores de credenciales invalidas?"
    ids_relevantes = {"d195eb84-4072-44b9-b0df-c91be040a154","109f4e73-0b7b-4c38-905d-21ad65b27a2e"}

    retriever = vs.as_retriever(search_kwargs={"k":K})
    chunk =  retriever.invoke(pregunta) #consulta pregunta
    ids_recuperados = [c.id for c in chunk]

    precision = precision_at_k(ids_recuperados, ids_relevantes)
    print ("precision; ", precision)

    exhautividad =  recall_at_k(ids_recuperados, ids_relevantes)
    print ("Exhautividad: ", exhautividad)

    f1 = f1_score(precision, exhautividad)
    print("f1 score: ", f1)

    casos_evaluacion = [
        {"pregunta": "", "ids_relavantes": {"ids1", "ids2"}},
        {"pregunta": "", "ids_relavantes": {"ids1", "ids2"}},
        {"pregunta": "", "ids_relavantes": {"ids1", "ids2"}},
    ]