# bot/__init__.py
# Combina RuleEngine + LLM vía RunnableParallel
# Autor responsable de este archivo: Danilo Chite Quispe

from langchain_core.runnables import RunnableParallel, RunnableLambda
from bot.rules import RuleEngine
from bot.prompts import run_llm
from bot.schema import AnswerSchema


class MedBot:
    """Chatbot médico que fusiona reglas determinísticas y LLM.
    
    Autor de la clase y sus métodos: Danilo Chite Quispe
    """

    # --------------------------------------------------
    # Autor: Danilo Chite Quispe
    def __init__(self):
        """Inicializa RuleEngine y define las ramas Runnable."""
        self.rules = RuleEngine()  # instancia del motor de reglas

        # Runnable que ejecuta las reglas locales
        reglas_fn = RunnableLambda(
            lambda q: self.rules.inferir(q["pregunta"])
        )

        # Runnable que llama al LLM y valida la salida con Pydantic
        llm_fn = RunnableLambda(
            lambda q: run_llm(q["pregunta"])
        )

        # RunnableParallel ejecuta ambas ramas simultáneamente
        self.parallel: RunnableParallel = RunnableParallel(
            reglas=reglas_fn,
            llm=llm_fn,
        )

        # Saludos que se manejan sin pasar por el LLM
        self._GREET = {
            "hola", "buenas", "buenos dias",
            "buenas tardes", "buenas noches"
        }

    # --------------------------------------------------
    # Autor: Danilo Chite Quispe
    def chat(self, pregunta: str) -> AnswerSchema:
        """
        Procesa la consulta y devuelve un AnswerSchema estructurado.

        1. Si la entrada es un saludo simple → responde con cortesía.
        2. Ejecuta reglas + LLM en paralelo.
        3. Fusiona las respuestas tomando la de mayor nivel_confianza.
        """
        # —— 1 · Saludo corto ——
        if pregunta.lower().strip() in self._GREET:
            return AnswerSchema(
                diagnosticos=["No aplica"],
                nivel_confianza=0.2,
                recomendacion="¡Hola! Cuéntame tus síntomas para poder orientarte.",
            )

        # —— 2 · Ejecutar ramas en paralelo ——
        resultados = self.parallel.invoke({"pregunta": pregunta})
        reglas = resultados["reglas"]
        llm_out = resultados["llm"]

        # —— 3 · Fusión por confianza ——
        if llm_out["nivel_confianza"] < reglas["nivel_confianza"]:
            # Preferimos el diagnóstico de las reglas, 
            # pero conservamos la recomendación del LLM.
            merged = reglas | {"recomendacion": llm_out["recomendacion"]}
        else:
            merged = llm_out
            # Añadimos explicación de reglas cuando gana el LLM
            merged["explicacion"] = reglas.get("explicacion")

        return AnswerSchema(**merged)
