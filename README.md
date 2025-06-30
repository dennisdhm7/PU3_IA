# 🩺 Sistema Chatbot de Pre Diagnóstico Médico — MedBot-Triage

MedBot-Triage es un sistema de chatbot inteligente para orientación médica preliminar. Usa una combinación de reglas médicas y un modelo de lenguaje (LLM) para brindar posibles diagnósticos, niveles de confianza y recomendaciones, todo desde una interfaz conversacional sencilla y accesible por web.

---

## 👥 Integrantes del proyecto

- **Christian Dennis Hinojosa Mucho**
- **Danilo Chite Quispe**
- **Royser Villanueva Mamani**

---

## 🎯 Objetivo del proyecto

Diseñar un sistema basado en inteligencia artificial que permita brindar una orientación médica inicial (pre diagnóstico), simulando un triage básico en emergencias o en entornos de atención rápida, incluyendo atención prehospitalaria.

---

## 🧰 Tecnologías utilizadas

- **Python** — lenguaje principal
- **FastAPI** — servidor web y API
- **LangChain** — flujos LLM y recuperación (RAG)
- **OpenAI GPT-3.5 Turbo** — modelo generativo
- **FAISS** — búsqueda semántica en documentos
- **Tailwind CSS + JavaScript** — frontend moderno
- **Pydantic** — validación de datos estructurados
- **dotenv** — gestión de variables de entorno

---

## 🚀 Instrucciones para ejecutar el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/medbot-triage.git
cd medbot-triage
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
.venv\Scripts\activate   # En Windows
# source .venv/bin/activate   # En Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la API Key

Crea un archivo `.env` en la raíz del proyecto con tu clave de OpenAI:

```
OPENAI_API_KEY=sk-...
```

### 5. Agregar documentos médicos

Coloca tus documentos en formato PDF dentro de la carpeta:

```
data/raw_pdfs/
```

Ejemplo: protocolos médicos, guías de atención, manuales de emergencia.

### 6. Construir el índice semántico (solo una vez)

```bash
python index_pdfs.py
```

Esto genera un índice en `data/vectorstore` para búsquedas con RAG.

### 7. Ejecutar el servidor

```bash
uvicorn api:app --reload
```

Luego, abre el navegador y visita:

```
http://127.0.0.1:8000
```

---

## 🧠 ¿Qué hace MedBot-Triage?

- Interpreta preguntas con síntomas y devuelve:
  - Diagnóstico sugerido
  - Nivel de confianza
  - Recomendación médica inicial

- Utiliza dos estrategias en paralelo:
  - **Motor de reglas médicas** (por palabras clave)
  - **Modelo de lenguaje** (GPT-3.5 con contexto de guías médicas)

- Aplica **RAG** (retrieval-augmented generation): si cargaste documentos PDF médicos, el bot usará esos textos como base para sus respuestas.

---

## ✨ Características destacadas

- ✅ Arquitectura orientada a objetos
- ✅ Funciones ejecutables (`RunnableParallel`)
- ✅ Combina reglas + LLM para mayor precisión
- ✅ Uso de patrones de diseño
- ✅ Interfaz conversacional moderna
- ✅ Reconocimiento de saludos y errores semánticos
- ✅ Modo claro / oscuro
- ✅ Soporte para atención prehospitalaria (paramédicos)

---

## 📦 Estructura de carpetas

```
medbot/
│
├── bot/                # Lógica del chatbot (reglas, LLM, RAG)
│   ├── __init__.py
│   ├── prompts.py
│   ├── retriever.py
│   ├── rules.py
│   └── schema.py
│
├── data/
│   ├── raw_pdfs/       # PDF médicos (entrada)
│   └── vectorstore/    # Índice FAISS (generado)
│
├── static/             # Frontend HTML, CSS, JS
├── api.py              # Backend FastAPI
├── index_pdfs.py       # Script para crear vectorstore
├── .env                # Clave de API
└── requirements.txt    # Dependencias
```

---


---

## 🧾 Licencia

Este proyecto ha sido desarrollado exclusivamente con fines académicos para el curso de **Inteligencia Artificial**.
