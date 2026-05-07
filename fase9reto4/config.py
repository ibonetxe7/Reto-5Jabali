import os
from dotenv import load_dotenv

load_dotenv()
# Configuración de la base de datos donde todo viene del .env por eso no se ve las contraseñas.
DB_CONFIG = {
    'host':     os.getenv('DB_HOST'),
    'user':     os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}
# Token de Hugging Face para acceder a los modelos de IA
HF_TOKEN = os.getenv('HF_TOKEN')
