# bot/prompts.py
# Autor: Christian Dennis Hinojosa Mucho
# Este módulo define el prompt base y la ejecución del LLM junto con el contexto recuperado.

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from bot.schema import AnswerSchema
from bot.retriever import busca_contexto

# Autor: Christian Dennis Hinojosa Mucho
# Instancia del modelo de lenguaje de OpenAI con baja temperatura para respuestas más determinísticas.
_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Autor: Christian Dennis Hinojosa Mucho
# Plantilla de prompt que instruye al LLM a responder siempre en formato JSON.
# Incluye ejemplos de few-shot para guiar al modelo.
_PROMPT = ChatPromptTemplate.from_messages([
    # Mensaje del sistema define el rol del asistente
    ("system",
     "Eres un asistente médico que orienta al usuario. "
     "No sustituyes a un profesional. Devuelve SIEMPRE JSON con las llaves "
     "diagnosticos, nivel_confianza y recomendacion. "
     "En 'recomendacion' entrega de 2 a 4 indicaciones concretas, separadas por punto y coma."),
    
    # Ejemplo 1: caso claro de COVID-19
    ("human",
     "Tengo fiebre y tos seca, ¿qué podría tener?"),
    ("ai",
     '{{"diagnosticos":["Posible COVID-19"],'
     '"nivel_confianza":0.8,'
     '"recomendacion":"Aíslate y consulta a un médico si los síntomas empeoran."}}'),

    # Ejemplo 2: resfriado común
    ("human", "Tengo congestión nasal y estornudos leves."),
    ("ai",
    '{{"diagnosticos":["Resfriado común"],'
    '"nivel_confianza":0.35,'
    '"recomendacion":"Descansa e hidrátate."}}'),

    # Ejemplo 3: síntomas más graves
    ("human", "Tengo fiebre de 39 °C y tos seca intensa."),
    ("ai",
    '{{"diagnosticos":["Probable COVID-19"],'
    '"nivel_confianza":0.85,'
    '"recomendacion":"Hazte una prueba y aíslate."}}'),

    # Plantilla donde se inserta la pregunta del usuario real
    ("human", "{pregunta}")
])

# Autor: Christian Dennis Hinojosa Mucho
def run_llm(pregunta: str) -> dict:
    """
    Ejecuta la búsqueda de contexto relevante (RAG),
    alimenta el prompt combinado al LLM,
    y valida que la respuesta sea JSON estructurado.
    """
    # Busca contexto vectorial para enriquecer la respuesta
    contexto = busca_contexto(pregunta, k=3)

    # Invoca el modelo con la plantilla y el contexto
    msg = (_PROMPT | _llm).invoke({"pregunta": pregunta, "contexto": contexto})

    # Extrae y valida la salida como JSON usando Pydantic
    raw_json = msg.content
    return AnswerSchema.model_validate_json(raw_json).dict()
