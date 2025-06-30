# bot/rules.py
# Autor: Danilo Chite Quispe
# Este módulo define un motor experto simple basado en reglas por palabras clave para diagnóstico médico preliminar.

from typing import Dict, List, Tuple

class RuleEngine:
    """
    Motor experto basado en reglas definidas manualmente.
    Busca coincidencias de síntomas y retorna diagnósticos sugeridos junto con un nivel de confianza y una explicación.
    """

    # Diccionario estático de reglas.
    # Cada regla tiene:
    #   - "all": síntomas obligatorios
    #   - "any": síntomas opcionales
    #   - "score": nivel de confianza asignado si se cumple la condición
    _REGLAS: Dict[str, Dict[str, List[str] | float]] = {
        "Alergia": {
            "all": ["estornudo", "picazón"],
            "any": ["congestión", "mocos", "lagrimeo"],
            "score": 0.6,
        },
        "Probable COVID-19": {
            "all": ["fiebre", "tos seca"],
            "any": ["cansancio", "dolor de cabeza", "pérdida de olfato"],
            "score": 0.8,
        },
        "Gripe común": {
            "all": ["dolor", "garganta"],
            "any": ["fiebre", "congestión", "cansancio"],
            "score": 0.5,
        },
        "Resfriado": {
            "all": ["congestión"],
            "any": ["estornudo", "mocos", "goteo nasal"],
            "score": 0.4,
        },
        "Bronquitis": {
            "all": ["tos", "flema"],
            "any": ["opresión", "pecho", "silbido"],
            "score": 0.7,
        },
        "Gastroenteritis": {
            "all": ["diarrea"],
            "any": ["vómito", "dolor abdominal", "nauseas"],
            "score": 0.65,
        },
        "Migraña": {
            "all": ["dolor de cabeza"],
            "any": ["nauseas", "fotofobia", "aura"],
            "score": 0.55,
        },
    }

    # ---------------------------------------------------------------------
    # Método privado para validar si un texto cumple con una regla
    def _match_regla(self, texto: str, regla: Dict) -> Tuple[bool, float]:
        # Cumple si contiene todos los síntomas obligatorios (all)
        cumple_all = all(k in texto for k in regla.get("all", []))
        # Y al menos uno de los opcionales (any), si existen
        cumple_any = not regla.get("any") or any(k in texto for k in regla.get("any", []))
        return cumple_all and cumple_any, regla["score"]

    # Método principal que aplica todas las reglas al texto del usuario
    def inferir(self, texto: str) -> Dict:
        texto = texto.lower()  # Normaliza el texto
        candidatos = []        # Guarda diagnósticos posibles
        detalles = []          # Guarda explicaciones

        # Itera por cada enfermedad y evalúa si la consulta coincide
        for patolog, regla in self._REGLAS.items():
            ok, sc = self._match_regla(texto, regla)
            if ok:
                candidatos.append((patolog, sc))
                detalles.append(
                    f"✔ {patolog} (score {sc}) — "
                    f"ALL={regla['all']}, ANY={regla['any']}"
                )

        # Si no hay coincidencias, se devuelve un resultado indeterminado
        if not candidatos:
            return {
                "diagnosticos": ["Indeterminado"],
                "nivel_confianza": 0.2,
                "explicacion": "No hubo coincidencias claras con las reglas.",
            }

        # Ordena candidatos por mayor score y prepara la respuesta estructurada
        candidatos.sort(key=lambda x: x[1], reverse=True)
        patos, scores = zip(*candidatos)

        return {
            "diagnosticos": list(patos),             # Lista ordenada de diagnósticos
            "nivel_confianza": scores[0],            # Mayor score de coincidencia
            "explicacion": "\n".join(detalles),      # Cómo se llegó al resultado
        }
