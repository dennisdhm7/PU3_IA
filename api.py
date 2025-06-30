# api.py
# Autor: Christian Dennis Hinojosa Mucho
# Archivo principal de entrada de la API. Usa FastAPI para exponer el backend del chatbot.

from dotenv import load_dotenv
load_dotenv()  # Carga la variable OPENAI_API_KEY desde el archivo .env (antes de usar cualquier componente LLM)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from bot import MedBot                      # Importa la clase del chatbot con lógica fusionada (reglas + LLM)
from bot.schema import PreguntaSchema       # Modelo para validar la entrada del usuario

bot = MedBot()                              # Instancia única del chatbot
app = FastAPI(title="MedBot-Triage")        # Crea aplicación FastAPI con título personalizado

# ---------- API ----------
@app.post("/chat")
async def chat(req: Request):
    """
    Endpoint principal para el chat.
    Recibe JSON del frontend, lo convierte en una pregunta usando PreguntaSchema,
    pasa la pregunta a MedBot y devuelve una respuesta estructurada.
    """
    body = await req.json()
    pregunta = PreguntaSchema(**body).texto   # Extrae el texto usando el alias 'question'
    respuesta = bot.chat(pregunta)            # Genera la respuesta desde la clase MedBot
    return JSONResponse(respuesta.model_dump(mode="json"))  # Devuelve como JSON

@app.get("/health")
def health():
    """Endpoint de prueba para verificar si la API está activa."""
    return {"status": "ok"}

# ---------- Frontend ----------
# Monta la carpeta 'static' como recurso estático (donde vive el frontend con HTML+JS+CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    """Cuando el usuario accede a '/', se sirve el archivo HTML del chatbot."""
    return FileResponse("static/index.html")
