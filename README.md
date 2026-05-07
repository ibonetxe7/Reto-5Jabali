#  JABALI — Gestión de Recetas con Inteligencia Artificial

  PARA DESCARGAR LOS ARCHIVOS TIENES QUE IR A LA BRANCH `RETO5pagina`** y ahí estaría todo.

---

##  Introducción

**JABALI** es una aplicación web desarrollada con **Flask (Python)** y **MySQL** que permite a los usuarios gestionar sus recetas de cocina de forma inteligente.

Los usuarios pueden registrarse, iniciar sesión, crear y eliminar sus propias recetas, y acceder a tres funcionalidades de **Inteligencia Artificial** que les ayudan a:
- Obtener **sugerencias de recetas** basadas en los ingredientes que tienen en casa.
- Generar un **menú semanal personalizado** según sus preferencias alimentarias.
- **Analizar el valor nutricional** de una receta y recibir consejos para mejorarla.

Todo el sistema está pensado para ser ligero, seguro (contraseñas cifradas con SHA-256) y fácil de desplegar en local.

---

##  Cómo funciona

Cuando el usuario abre la aplicación en su navegador, Flask recibe la petición y la dirige a la ruta correspondiente en `app.py`. Dependiendo de la acción, Flask consulta la base de datos MySQL para leer o guardar información, o llama a `ia.py` para generar una respuesta con IA.

El flujo principal es:

```
Navegador → Flask (app.py) → MySQL (datos) / ia.py (IA) → HTML renderizado → Navegador
```

La IA se comunica con la API de **Hugging Face** usando el modelo **Meta-Llama-3.3-70B-Instruct**, que recibe un prompt en español y devuelve una respuesta de texto que se muestra directamente al usuario.

---

##  Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                    NAVEGADOR                        │
│            http://127.0.0.1:5000                    │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP Request
┌─────────────────────▼───────────────────────────────┐
│                  FLASK (app.py)                     │
│                                                     │
│  /           → RETO5.html (inicio)                  │
│  /registro   → Registro de usuario                  │
│  /login      → Inicio de sesión                     │
│  /tusrecetas → Ver recetas del usuario              │
│  /pontureceta → Crear nueva receta                  │
│  /ia/sugerencia → IA: sugerir receta                │
│  /ia/menu       → IA: menú semanal                  │
│  /ia/analisis   → IA: análisis nutricional          │
└──────────┬──────────────────────┬───────────────────┘
           │                      │
┌──────────▼──────────┐  ┌────────▼────────────────────┐
│   MySQL (jabali)    │  │     Hugging Face API         │
│                     │  │  Meta-Llama-3.3-70B-Instruct │
│  USUARIO            │  │                              │
│  CLIENTE            │  │  ia.py                       │
│  RECETA             │  │  ├── sugerir_receta()        │
│  INGREDIENTE        │  │  ├── generar_menu_semanal()  │
│  RECETA_INGREDIENTE │  │  └── analizar_nutriscore()   │
└─────────────────────┘  └──────────────────────────────┘
```

---

##  Estructura del proyecto

```
└── fase9reto4/
    ├── app.py              # Rutas y lógica principal
    ├── config.py           # Lee las variables del .env
    ├── ia.py               # Funciones de inteligencia artificial
    ├── JABALÍ.sql          # Script para crear la base de datos
    ├── .env                # Variables de entorno (NO subir a GitHub)
    ├── .gitignore          # Archivos ignorados por Git
    ├── templates/          # Páginas HTML (Jinja2)
    │   ├── RETO5.html          # Página principal
    │   ├── login.html
    │   ├── registro.html
    │   ├── pontureceta.html
    │   ├── tusrecetas.html
    │   ├── recetas.html
    │   └── menu_semanal.html
    └── static/             # CSS e imágenes
        ├── color.css
        ├── menu_semanal.css
        ├── pontureceta.css
        ├── recetas.css
        ├── tusrecetas.css
        └── logo.jpeg
```

---

##  Tecnologías utilizadas

### Lenguaje
- **Python 3**

### Framework web
- **Flask** — gestiona las rutas, sesiones y renderizado de plantillas HTML con Jinja2.

### Base de datos
- **MySQL** — almacena usuarios, clientes, recetas e ingredientes.
- **flask-mysqldb** — conector entre Flask y MySQL.

### Inteligencia Artificial
- **Hugging Face API** — servicio externo de IA.
- **Meta-Llama-3.3-70B-Instruct** — modelo de lenguaje que genera las respuestas.
- **requests** — librería Python para hacer las llamadas HTTP a la API.

### Seguridad
- **hashlib (SHA-256)** — cifra las contraseñas antes de guardarlas en la base de datos.
- **python-dotenv** — carga las credenciales desde un archivo `.env` para no exponerlas en el código.

### Herramientas
- IDE: **VSCode**
- Cliente MySQL: **MySQL Workbench**

---

##  Base de datos

El archivo SQL está en la raíz del proyecto:

```
└── JABALÍ.sql   # Crea todas las tablas e inserta los datos iniciales
```

Tablas principales:

| Tabla | Contenido |
|-------|-----------|
| `USUARIO` | Datos personales (nombre, email, teléfono) |
| `CLIENTE` | Credenciales y contadores (logins, recetas) |
| `RECETA` | Recetas creadas por cada usuario |
| `INGREDIENTE` | Ingredientes con info de sostenibilidad y caducidad |
| `RECETA_INGREDIENTE` | Relación entre recetas e ingredientes |

> Antes de arrancar la app, abre `JABALÍ.sql` en **MySQL Workbench** y ejecútalo.

---

##  Instalación y puesta en marcha

### 1. Clona el repositorio y cambia a la branch correcta

```bash
git clone https://github.com/ibonetxe7/Reto-5Jabali.git
cd Reto-5Jabali
git checkout RETO5pagina
```

### 2. Instala las dependencias

```bash
pip install flask
pip install flask_mysqldb
pip install python-dotenv
pip install requests
```

### 3. Crea el archivo `.env` en la raíz del proyecto

```dotenv
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=jabali
HF_TOKEN=tu_token_de_huggingface
```

- `DB_PASSWORD` → tu contraseña de MySQL
- `HF_TOKEN` → tu token de [Hugging Face](https://huggingface.co/settings/tokens)

>  **Nunca subas el `.env` a GitHub**, ya está en el `.gitignore`.

### 4. Ejecuta la base de datos

Abre `JABALÍ.sql` en MySQL Workbench y ejecútalo para crear todas las tablas.

### 5. Arranca la aplicación

```bash
python app.py
```

### 6. Abre el navegador en

```
http://127.0.0.1:5000
```

---

##  Funcionalidades

-  Registro e inicio de sesión con contraseña cifrada (SHA-256)
-  Crear, ver y eliminar recetas con ingredientes
-  IA para sugerir recetas según ingrediente y nutriscore
-  IA para generar menú semanal personalizado
-  IA para analizar el valor nutricional de una receta
-  Formulario de contacto
-  Control de sesión (no puedes acceder sin login)

---
 Uso de IA en el desarrollo
Durante el desarrollo del proyecto usamos Inteligencia Artificial como ayuda para resolver partes que no sabíamos hacer solos:

Cifrado de contraseñas — No sabíamos cómo proteger las contraseñas de los usuarios ante un posible hackeo. La IA nos explicó cómo usar hashlib con el algoritmo SHA-256, que convierte la contraseña en bytes y la transforma en un hash irreversible antes de guardarla en la base de datos.
Conexión con Hugging Face en ia.py — No teníamos claro cómo conectar nuestra app con un modelo de lenguaje externo. La IA nos guió para hacer llamadas HTTP a la API de Hugging Face usando requests, configurar las cabeceras con el token de autenticación y manejar los posibles errores de respuesta (503, 401, timeout...).
Consultas SQL complejas — Para algunas consultas con varios JOIN entre tablas (como la de tusrecetas que une RECETA, INGREDIENTE y RECETA_INGREDIENTE), usamos la IA para estructurar correctamente el GROUP BY y evitar duplicados.


##  Autores

| Ibon YE | Unax Gahona | Ibon Etxegia | Xabier Morales |

