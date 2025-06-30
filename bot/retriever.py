# bot/retriever.py
# Autor: Royser Villanueva Mamani
# Este módulo se encarga de buscar contexto relevante desde PDFs indexados mediante FAISS para enriquecer las respuestas del chatbot.

from langchain_community.vectorstores import FAISS  # Librería para recuperar información vectorizada
from langchain_openai import OpenAIEmbeddings       # Embeddings de OpenAI para consulta semántica
import os                                           # Módulo estándar para manejo de rutas

# Autor: Royser Villanueva Mamani
# Ruta donde se almacenan los vectores FAISS generados a partir de los PDFs.
_VEC_DIR = "data/vectorstore"

# Verifica si el directorio del índice existe; si no, se lanza un error indicando que primero debe ejecutarse el script de indexado.
if not os.path.isdir(_VEC_DIR):
    raise RuntimeError(
        f"No existe {_VEC_DIR}. Ejecuta primero 'python index_pdfs.py'."
    )

# Carga el índice FAISS previamente creado con los embeddings generados.
# Se habilita la deserialización peligrosa confiando en el entorno local controlado.
_store = FAISS.load_local(
    _VEC_DIR,
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True   # CONFIRMAS que confías en el pickle
)

# Autor: Royser Villanueva Mamani
def busca_contexto(pregunta: str, k: int = 3) -> str:
    """
    Realiza una búsqueda semántica en el índice vectorial FAISS
    para recuperar los k documentos más relevantes relacionados con la pregunta.

    Parámetros:
        pregunta (str): Texto ingresado por el usuario.
        k (int): Número de documentos similares a recuperar (por defecto 3).

    Retorna:
        str: Cadena de texto con el contenido concatenado de los documentos relevantes.
    """
    docs = _store.similarity_search(pregunta, k=k)
    return "\n\n".join(d.page_content for d in docs)
