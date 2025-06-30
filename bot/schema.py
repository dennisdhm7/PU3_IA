# bot/schema.py
# Autor: Royser Villanueva Mamani
# Este módulo define los esquemas de validación (modelos de datos) que usa el chatbot para procesar entradas y estructurar salidas.

from pydantic import BaseModel, Field
from typing import List

class PreguntaSchema(BaseModel):
    """
    Modelo que define cómo se debe recibir la pregunta desde el frontend.
    Acepta un campo llamado 'question' (alias de 'descripcion') que puede ser None.
    """
    descripcion: str | None = Field(None, alias="question")  # Alias permite recibir 'question' desde JSON del frontend

    @property
    def texto(self) -> str:
        """
        Propiedad para extraer el texto de la pregunta.
        Si no hay descripción, devuelve cadena vacía.
        """
        return self.descripcion or ""

class AnswerSchema(BaseModel):
    """
    Modelo de respuesta estructurada que el backend envía al frontend.
    Incluye diagnóstico(s), nivel de confianza, recomendación y explicación opcional.
    """
    diagnosticos: List[str]            # Lista de posibles enfermedades detectadas
    nivel_confianza: float             # Porcentaje de certeza del análisis
    recomendacion: str                 # Consejos de cuidado o pasos a seguir
