import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")

def construir_prompt(ingredientes: list) -> str:
    lista = ", ".join(ingredientes)
    return f"""Eres un chef experto. El usuario tiene estos ingredientes disponibles: {lista}.
Genera una receta usando solo esos ingredientes (puedes asumir sal, aceite y agua).
Responde ÚNICAMENTE con un JSON válido con esta estructura exacta, sin texto adicional, sin backticks:
{{
  "nombre_plato": "string",
  "ingredientes": [{{"nombre": "string", "cantidad": "string"}}],
  "pasos": ["paso 1", "paso 2"],
  "tiempo_estimado": "string",
  "dificultad": "fácil"
}}"""

def generar_receta(ingredientes: list) -> dict:
    prompt = construir_prompt(ingredientes)
    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Generador de Recetas"
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        },
        timeout=60.0
    )
    response.raise_for_status()
    contenido = response.json()["choices"][0]["message"]["content"]
    # Limpiar posibles backticks de markdown
    contenido = contenido.strip()
    if contenido.startswith("```"):
        contenido = contenido.split("```")[1]
        if contenido.startswith("json"):
            contenido = contenido[4:]
    contenido = contenido.strip()
    return json.loads(contenido)