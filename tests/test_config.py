import pytest
from unittest.mock import patch
import os
# gahona: verifica que la configuración de la base de datos se carga bien
@patch.dict(os.environ, {
    'DB_HOST': 'localhost',
    'DB_USER': 'root',
    'DB_PASSWORD': '1234',
    'DB_NAME': 'jabali',
    'HF_TOKEN': 'token_prueba'
})
def test_db_config_carga_bien():
    import importlib
    import config
    importlib.reload(config)

    assert config.DB_CONFIG['host'] == 'localhost'
    assert config.DB_CONFIG['user'] == 'root'
    assert config.DB_CONFIG['password'] == '1234'
    assert config.DB_CONFIG['database'] == 'jabali'
# gahona: verifica que el token de HuggingFace se carga correctamente
@patch.dict(os.environ, {
    'DB_HOST': 'localhost',
    'DB_USER': 'root',
    'DB_PASSWORD': '1234',
    'DB_NAME': 'jabali',
    'HF_TOKEN': 'token_prueba'
})
def test_hf_token_carga_bien():
    import importlib
    import config
    importlib.reload(config)

    assert config.HF_TOKEN == 'token_prueba'
# gahona: verifica que DB_CONFIG tiene las claves esperadas
@patch.dict(os.environ, {
    'DB_HOST': 'localhost',
    'DB_USER': 'root',
    'DB_PASSWORD': '1234',
    'DB_NAME': 'jabali',
    'HF_TOKEN': 'token_prueba'
})
def test_db_config_tiene_todas_las_claves():
    import importlib
    import config
    importlib.reload(config)

    assert set(config.DB_CONFIG.keys()) == {'host', 'user', 'password', 'database'}