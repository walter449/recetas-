import pytest
import json
from unittest.mock import patch, MagicMock
from app.services.llm_service import construir_prompt, generar_receta
from app.schemas.schemas import IngredienteCreate, CalificacionCreate

# Test 1: Validación de ingredientes - nombre vacío
def test_ingrediente_nombre_no_vacio():
    with pytest.raises(Exception):
        ing = IngredienteCreate(nombre="", cantidad="100", unidad="g")
        assert ing.nombre != ""

# Test 2: Validación de calificación fuera de rango
def test_calificacion_rango_invalido():
    cal = CalificacionCreate(estrellas=6)
    assert not (1 <= cal.estrellas <= 5)

# Test 3: Calificación válida
def test_calificacion_rango_valido():
    cal = CalificacionCreate(estrellas=4)
    assert 1 <= cal.estrellas <= 5

# Test 4: Prompt contiene los ingredientes
def test_prompt_contiene_ingredientes():
    ingredientes = ["tomate", "queso", "pasta"]
    prompt = construir_prompt(ingredientes)
    for ing in ingredientes:
        assert ing in prompt

# Test 5: Prompt pide JSON
def test_prompt_pide_json():
    prompt = construir_prompt(["arroz"])
    assert "JSON" in prompt
    assert "nombre_plato" in prompt

# Test 6: Parseo correcto de respuesta del LLM
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