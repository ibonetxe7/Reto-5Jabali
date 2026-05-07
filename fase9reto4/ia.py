import requests
from config import HF_TOKEN
#Hemos usado aqui la IA porque no sabiamos como conectar la IA con la aplicacion.
API_URL = "https://router.huggingface.co/sambanova/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}


def _llamar_ia(prompt, max_tokens=300):
    try:
        r = requests.post(API_URL, headers=HEADERS, timeout=30, json={
            "model": "Meta-Llama-3.3-70B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens
        })

        if r.status_code== 503: return "El modelo está cargando, espera 20 segundos."
        if r.status_code == 401: return"Token inválido. Revisa tu .env"
        if r.status_code!= 200: return f"Error {r.status_code}: {r.text[:200]}"

        return r.json()['choices'][0]['message']['content'].strip()

    except requests.exceptions.Timeout:
        return " La IA tardó demasiado. Inténtalo de nuevo."
    except Exception as e:
        return f" Error: {e}"

#El max_tokens es el número máximo de tokens que la IA puede generar en su respuesta.Son las palabras que te dan mas o menos
def sugerir_receta(ingrediente, nutriscore):
    prompt = f"Eres un dietista. Sugiere UNA receta con {ingrediente} (nutriscore {nutriscore}): nombre, ingredientes y 3 pasos. En español."
    return _llamar_ia(prompt, max_tokens=300)
    #El prompt es lo que le decimos a la IA para que nos genere la respuesta que queremos. En este caso, le decimos que sea un dietista y que nos sugiera una receta con un ingrediente y un nutriscore determinado. 

def generar_menu_semanal(preferencias):
    prompt = f"Eres un dietista. Crea un menú semanal (lunes-domingo) con desayuno, comida y cena para: {preferencias}. En español."
    return _llamar_ia(prompt, max_tokens=500)



def analizar_nutriscore(nombre_receta, valor_nutricional, nutriscore):
    prompt = f"Eres un nutricionista. Analiza: {nombre_receta}, {valor_nutricional} kcal, nutriscore {nutriscore}. Da 3 consejos para mejorarla. En español."
    return _llamar_ia(prompt, max_tokens=250)
