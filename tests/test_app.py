import pytest
import json
from unittest.mock import patch, MagicMock
from app.services.llm_service import construir_prompt, generar_receta
from app.schemas.schemas import IngredienteCreate, CalificacionCreate


# Test 1: El prompt contiene los ingredientes
def test_prompt_contiene_ingredientes():
    ingredientes = ["tomate", "queso", "pasta"]
    prompt = construir_prompt(ingredientes)
    for ing in ingredientes:
        assert ing in prompt


# Test 2: El prompt pide respuesta en JSON
def test_prompt_pide_json():
    prompt = construir_prompt(["arroz"])
    assert "JSON" in prompt
    assert "nombre_plato" in prompt


# Test 3: El prompt incluye todos los campos requeridos
def test_prompt_incluye_campos_requeridos():
    prompt = construir_prompt(["pollo"])
    assert "ingredientes" in prompt
    assert "pasos" in prompt
    assert "tiempo_estimado" in prompt
    assert "dificultad" in prompt


# Test 4: Parseo correcto de respuesta del LLM
def test_parseo_respuesta_llm():
    receta_mock = {
        "nombre_plato": "Arroz con huevo",
        "ingredientes": [{"nombre": "arroz", "cantidad": "1 taza"}],
        "pasos": ["Hervir el arroz", "Freír el huevo"],
        "tiempo_estimado": "20 minutos",
        "dificultad": "fácil"
    }
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": json.dumps(receta_mock)}}]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.post", return_value=mock_response):
        resultado = generar_receta(["arroz", "huevo"])
        assert resultado["nombre_plato"] == "Arroz con huevo"
        assert len(resultado["pasos"]) == 2
        assert resultado["dificultad"] == "fácil"


# Test 5: Parseo limpia backticks de markdown
def test_parseo_limpia_markdown():
    receta_mock = {
        "nombre_plato": "Sopa",
        "ingredientes": [{"nombre": "agua", "cantidad": "1L"}],
        "pasos": ["Hervir el agua"],
        "tiempo_estimado": "10 minutos",
        "dificultad": "fácil"
    }
    contenido_con_backticks = f"```json\n{json.dumps(receta_mock)}\n```"
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": contenido_con_backticks}}]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.post", return_value=mock_response):
        resultado = generar_receta(["agua"])
        assert resultado["nombre_plato"] == "Sopa"


# Test 6: Validación de calificación válida
def test_calificacion_valida():
    cal = CalificacionCreate(estrellas=4)
    assert 1 <= cal.estrellas <= 5


# Test 7: Calificación fuera de rango
def test_calificacion_fuera_de_rango():
    cal = CalificacionCreate(estrellas=6)
    assert not (1 <= cal.estrellas <= 5)


# Test 8: Ingrediente tiene los campos correctos
def test_ingrediente_campos_correctos():
    ing = IngredienteCreate(nombre="tomate", cantidad="3", unidad="unidades")
    assert ing.nombre == "tomate"
    assert ing.cantidad == "3"
    assert ing.unidad == "unidades"