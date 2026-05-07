## test_ia.py

import pytest
from unittest.mock import patch, MagicMock
from ia import _llamar_ia, sugerir_receta, generar_menu_semanal, analizar_nutriscore

@pytest.fixture
def mock_respuesta_ok():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {'choices': [{'message': {'content': 'OK'}}]}
    return mock

# gahona: verifica que _llamar_ia funciona con respuesta OK
@patch('ia.requests.post')
def test_llamar_ia_correcta(mock_post, mock_respuesta_ok):
    mock_post.return_value = mock_respuesta_ok
    assert _llamar_ia('test') == 'OK'

# gahona: verifica que sugerir_receta construye bien el prompt
@patch('ia._llamar_ia')
def test_sugerir_receta_usa_ingrediente(mock_ia):
    mock_ia.return_value = 'receta'
    sugerir_receta('pollo', 'A')
    prompt = mock_ia.call_args[0][0]
    assert 'pollo' in prompt and 'A' in prompt

# gahona: verifica menu semanal usa 500 tokens
@patch('ia._llamar_ia')
def test_generar_menu_max_tokens(mock_ia):
    mock_ia.return_value = 'menu'
    generar_menu_semanal('equilibrada')
    assert mock_ia.call_args[1]['max_tokens'] == 500

# gahona: verifica análisis nutriscore incluye datos receta
@patch('ia._llamar_ia')
def test_analizar_nutriscore_usa_datos_receta(mock_ia):
    mock_ia.return_value = 'analisis'
    analizar_nutriscore('Tortilla', '350', 'B')
    prompt = mock_ia.call_args[0][0]
    assert 'Tortilla' in prompt and '350' in prompt