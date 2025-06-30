# index_pdfs.py
# Autor: Christian Dennis Hinojosa Mucho
# Este script carga archivos PDF, los divide en fragmentos de texto (chunks),
# genera sus embeddings y guarda un índice FAISS para su uso posterior por el chatbot.

from dotenv import load_dotenv
load_dotenv()  # Carga las variables de entorno, especialmente OPENAI_API_KEY

# Importa utilidades de LangChain para procesar PDFs y generar embeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Utilidades estándar para manejo de archivos
import glob, os, pathlib

# Definición de rutas: carpeta con PDFs y carpeta para guardar el índice vectorial
RAW_DIR = "data/raw_pdfs"
VEC_DIR = "data/vectorstore"

def main():
    print("🛈  Cargando PDFs…")
    docs = []
    # Busca todos los archivos PDF en la carpeta RAW_DIR y los carga como documentos LangChain
    for pdf in glob.glob(os.path.join(RAW_DIR, "*.pdf")):
        docs.extend(PyPDFLoader(pdf).load())
    print(f"  → {len(docs)} páginas.")  # Cantidad total de páginas procesadas

    print("🛈  Dividiendo en chunks…")
    # Divide los documentos en fragmentos manejables para el modelo LLM
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    chunks = splitter.split_documents(docs)
    print(f"  → {len(chunks)} fragmentos.")

    print("🛈  Generando embeddings y construyendo índice FAISS…")
    # Genera embeddings usando OpenAI y crea un índice FAISS para búsquedas semánticas
    store = FAISS.from_documents(chunks, OpenAIEmbeddings())

    # Crea la carpeta si no existe y guarda el índice vectorial
    pathlib.Path(VEC_DIR).mkdir(parents=True, exist_ok=True)
    store.save_local(VEC_DIR)
    print("✅  Vectorstore guardado en", VEC_DIR)

# Ejecuta la función principal si se lanza como script
if __name__ == "__main__":
    main()
