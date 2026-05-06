
Aplicación web de gestión de recetas con inteligencia artificial. Desarrollada con Flask y MySQL.

---

Tecnologías utilizadas

 Lenguajes de programación
- Python 

 Base de datos
- MySQL

 Librerías 
- `Flask`
- `flask-mysqldb`
- `python-dotenv`
- `hashlib`

  Herramientas y Entorno
- IDE: VSCode
- Cliente MySQL: MySQL Workbench

Base de datos

El archivo de la base de datos está en la carpeta `base_de_datos`:

```
└── base_de_datos/
    └── jabali.sql   # Crea todas las tablas e inserta los datos iniciales
```

Antes de arrancar la app ejecuta `jabali.sql` en MySQL Workbench.

Aplicación web (Flask)

El archivo principal es `app.py` y está en la raíz del proyecto:

```
└── jabali/
    ├── app.py              # Rutas y lógica principal
    ├── config.py           # Lee la configuración del .env
    ├── ia.py               # Funciones de inteligencia artificial
    ├── .env                # Variables de entorno (no subir a GitHub)
    ├── requirements.txt    # Dependencias
    ├── templates/          # Páginas HTML
    └── static/             # CSS, imágenes y JS
```

# Pasos a seguir

1. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    pip install flask
    pip install flask_mysqldb
    ```

2. Crea un archivo `.env` en la carpeta raíz con este contenido:
    ```
    DB_HOST=127.0.0.1
    DB_USER=root
    DB_PASSWORD=tu_contraseña
    DB_NAME=jabali
    HF_TOKEN=tu_token_de_huggingface
    ```
    `DB_PASSWORD` → reemplaza `tu_contraseña` por tu contraseña de MySQL  
    `HF_TOKEN` → reemplaza `tu_token_de_huggingface` por tu token de Hugging Face

3. Ejecuta la base de datos: abre `jabali.sql` en MySQL Workbench y ejecútalo.

4. Arranca la aplicación:
    ```bash
    python app.py
    ```

5. Abre el navegador en [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

Funcionalidades

- Registro e inicio de sesión con contraseña cifrada
- Crear, ver y eliminar recetas con ingredientes
- IA para sugerir recetas según ingrediente y nutriscore
- IA para generar menú semanal personalizado
- IA para analizar el valor nutricional de una receta
- Formulario de contacto

---

Autores

**Ibon YE**  
**Unax Gahona**
**Ibon Etxegia**
**Xabier Morales**  

