from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from config import DB_CONFIG  # Archivo externo con los datos de conexión a la Base de datos
import hashlib  # Para encriptar contraseñas
from ia import sugerir_receta, generar_menu_semanal, analizar_nutriscore  # Funciones de IA propias

app = Flask(__name__)
app.secret_key = 'jabali_secret_key'  # Clave para firmar las sesiones de usuario

# Datos de conexión a la base de datos, del archivo config.py
app.config['MYSQL_HOST']     = DB_CONFIG['host']
app.config['MYSQL_USER']     = DB_CONFIG['user']
app.config['MYSQL_PASSWORD'] = DB_CONFIG['password']
app.config['MYSQL_DB']       = DB_CONFIG['database']
app.config['MYSQL_CHARSET']  = 'utf8mb4'  # Para que soporte tildes y emojis

mysql = MySQL(app)  # Conecta Flask con la base de datos


@app.route('/')
def index():
    return render_template('RETO5.html')  # Abre la página principal


@app.route('/contacto', methods=['POST'])
def contacto():
    # Recoge el nombre y email del formulario y elimina espacios extra con strip()
    nombre = request.form.get('nombre', '').strip()
    email  = request.form.get('email', '').strip()

    # Si falta alguno de los dos, devuelve un error sin tocar la BD
    if not nombre or not email:
        return render_template('RETO5.html', error_contacto='Nombre y email son obligatorios')

    try:
        cur = mysql.connection.cursor()  # Abre una consulta a la BD
        cur.execute("INSERT INTO USUARIO (nombre_usu, mail_usu) VALUES (%s, %s)", (nombre[:50], email))
        # nombre[:50] limita el texto a 50 caracteres para no pasarse del tamaño del campo en BD
        mysql.connection.commit()  # Guarda los cambios en la BD
        cur.close()
        return render_template('RETO5.html', ok_contacto='Mensaje enviado. Te contactaremos pronto.')
    except Exception as e:
        # Si algo falla al guardar, muestra el error en pantalla
        return render_template('RETO5.html', error_contacto=f'Error: {e}')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # Si el usuario solo visita la página (GET), simplemente la muestra
    if request.method == 'GET':
        return render_template('registro.html')

    # Recoge todos los campos del formulario
    nombre    = request.form.get('nombre', '').strip()
    apellido1 = request.form.get('apellido1', '').strip()
    apellido2 = request.form.get('apellido2', '').strip()
    email     = request.form.get('email', '').strip()
    telefono  = request.form.get('telefono', '').strip()
    password  = request.form.get('password', '')
    password2 = request.form.get('password', '')

    # Comprueba que los campos obligatorios no estén vacíos
    if not nombre or not apellido1 or not email or not password:
        return render_template('registro.html', error='Rellena todos los campos obligatorios.')

    # Comprueba que las dos contraseñas introducidas coincidan
    if password != password2:
        return render_template('registro.html', error='No coinciden las contraseñas.')

    # Si el teléfono no es un número válido, lo guarda como None (vacío) en lugar de dar error
    try:
        telefono_int = int(telefono) if telefono else None
    except ValueError:
        telefono_int = None

    # Encripta la contraseña con SHA-256 antes de guardarla
    # .encode() la convierte a bytes porque SHA-256 solo trabaja con bytes
    # .hexdigest() la convierte al resultado en texto
    # [:200] recorta a 200 caracteres por el límite del campo en BD
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()[:200]

    try:
        cur = mysql.connection.cursor()

        # Comprueba si ya existe un usuario con ese email
        cur.execute("SELECT id_usu FROM USUARIO WHERE mail_usu = %s", (email,))
        # fetchone() coge solo la primera fila; si existe algo, el email ya está en uso
        if cur.fetchone():
            cur.close()
            return render_template('registro.html', error='Ese email ya está en uso.')

        # Inserta el usuario en la tabla USUARIO
        cur.execute("""
            INSERT INTO USUARIO (nombre_usu, apellido1_usu, apellido2_usu, mail_usu, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre[:50], apellido1[:50], apellido2[:50] or None, email, telefono_int))

        # Inserta también en la tabla CLIENTE, usando el ID recién creado con lastrowid
        # lastrowid devuelve el ID del último INSERT ejecutado
        cur.execute("""
            INSERT INTO CLIENTE (id_usu, num_logs, num_recetas, contrasenia) VALUES (%s, 0, 0, %s)
        """, (cur.lastrowid, pwd_hash))

        mysql.connection.commit()
        cur.close()

    except Exception as e:
        # Si algo falla, deshace todos los cambios hechos en esta operación
        mysql.connection.rollback()
        return render_template('registro.html', error=f'Error al registrar: {e}')

    return redirect('/login')  # Si todo va bien, manda al usuario a iniciar sesión


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email    = request.form.get('email', '').strip()
    # Encripta la contraseña igual que al registrarse para poder compararlas
    pwd_hash = hashlib.sha256(request.form.get('password', '').encode()).hexdigest()[:200]

    try:
        cur = mysql.connection.cursor()
        # Busca un usuario cuyo email y contraseña encriptada coincidan con los introducidos
        # JOIN une las tablas USUARIO y CLIENTE para coger datos de las dos a la vez
        cur.execute("""
            SELECT u.id_usu, u.nombre_usu, c.id_cli
            FROM USUARIO u JOIN CLIENTE c ON u.id_usu = c.id_usu
            WHERE u.mail_usu = %s AND c.contrasenia = %s
        """, (email, pwd_hash))
        usuario = cur.fetchone()

        # Si no encuentra ningún usuario con esas credenciales, muestra error
        if not usuario:
            cur.close()
            return render_template('login.html', error='Email o contraseña incorrectos.')

        # Guarda los datos del usuario en la sesión para tenerlos disponibles en toda la app
        session['id_usu'] = usuario[0]
        session['nombre'] = usuario[1]
        session['id_cli'] = usuario[2]

        # Suma 1 al contador de veces que ha iniciado sesión
        # COALESCE evita errores si el campo es NULL, tratándolo como 0
        cur.execute("UPDA   TE CLIENTE SET num_logs = COALESCE(num_logs, 0) + 1 WHERE id_cli = %s", (usuario[2],))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        return render_template('login.html', error=f'Error de conexión: {e}')

    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/ia/sugerencia', methods=['POST'])
def ia_sugerencia():
    # Si no hay sesión activa, manda al login
    if not session.get('id_cli'):
        return redirect('/login')

    # Recoge lo que el usuario ha escrito y llama a la función de IA
    ingrediente = request.form.get('ingrediente', '')
    nutriscore  = request.form.get('nutriscore', 'C')
    resultado   = sugerir_receta(ingrediente, nutriscore)

    return render_template('RETO5.html',
        sugerencia_ia=resultado,
        ingrediente_ia=ingrediente,
        nutriscore_ia=nutriscore)


@app.route('/ia/guardar_receta', methods=['POST'])
def guardar_receta_ia():
    if not session.get('id_cli'):
        return redirect('/login')

    nombre_receta = request.form.get('nombre_receta', 'Receta IA')[:50]
    nutriscore    = request.form.get('nutriscore', 'C')[0].upper()  # Solo la primera letra en mayúscula
    id_cli        = session['id_cli']

    try:
        cur = mysql.connection.cursor()
        # Primero crea un ingrediente genérico con el nombre de la receta
        cur.execute("""
            INSERT INTO INGREDIENTE (nombre_ingrediente, sostenibilidad_producto, cecliaco)
            VALUES (%s, 'Nacional', 0)
        """, (nombre_receta,))

        # Luego guarda la receta en sí
        cur.execute("""
            INSERT INTO RECETA (id_cli, nombre_receta, nutriscore) VALUES (%s, %s, %s)
        """, (id_cli, nombre_receta, nutriscore))
        id_receta = cur.lastrowid

        # Relaciona la receta con el ingrediente recién creado
        # lastrowid - 1 apunta al ID del ingrediente insertado justo antes
        cur.execute("INSERT INTO RECETA_INGREDIENTE (id_receta, id_ingrediente) VALUES (%s, %s)", (id_receta, cur.lastrowid - 1))
        cur.execute("UPDATE CLIENTE SET num_recetas = COALESCE(num_recetas, 0) + 1 WHERE id_cli = %s", (id_cli,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        mysql.connection.rollback()
        return render_template('RETO5.html', error_receta=f'Error al guardar: {e}')

    return redirect('/tusrecetas')


@app.route('/ia/menu', methods=['POST'])
def ia_menu():
    if not session.get('id_cli'):
        return redirect('/login')

    # Llama a la función de IA con las preferencias del usuario para generar el menú
    preferencias = request.form.get('preferencias', 'equilibrada')
    menu = generar_menu_semanal(preferencias)
    return render_template('menu_semanal.html', menu_ia=menu)


@app.route('/ia/analisis', methods=['POST'])
def ia_analisis():
    if not session.get('id_cli'):
        return redirect('/login')

    # Recoge los datos de la receta y llama a la IA para analizarla
    nombre   = request.form.get('nombre_receta', '')
    kcal     = request.form.get('valor_nutricional', '0')
    score    = request.form.get('nutriscore', 'C')
    analisis = analizar_nutriscore(nombre, kcal, score)
    return render_template('RETO5.html', analisis_ia=analisis)


@app.route('/recetas')
def recetas():
    return render_template('recetas.html')


@app.route('/tusrecetas')
def tus_recetas():
    if not session.get('id_cli'):
        return redirect('/login')

    try:
        cur = mysql.connection.cursor()
        # Consulta todas las recetas del usuario con sus ingredientes
        # LEFT JOIN incluye recetas aunque no tengan ingredientes asociados
        # MIN/MAX agrupan varios ingredientes en una sola fila por receta
        # GROUP BY agrupa los resultados por receta para no repetir filas
        # ORDER BY id_receta DESC muestra las más recientes primero
        cur.execute("""
            SELECT r.id_receta, r.nombre_receta, r.valor_nutricional, r.nutriscore,
                   MIN(i.nombre_ingrediente), MIN(i.sostenibilidad_producto),
                   MAX(i.cecliaco), MIN(i.caducidad), r.fecha_creacion
            FROM RECETA r
            LEFT JOIN RECETA_INGREDIENTE ri ON r.id_receta = ri.id_receta
            LEFT JOIN INGREDIENTE i ON ri.id_ingrediente = i.id_ingrediente
            WHERE r.id_cli = %s
            GROUP BY r.id_receta, r.nombre_receta, r.valor_nutricional, r.nutriscore, r.fecha_creacion
            ORDER BY r.id_receta DESC
        """, (session['id_cli'],))
        rows = cur.fetchall()
        cur.close()

        # Convierte cada fila de la BD en un diccionario con nombres claros
        # para que en el HTML sea más fácil acceder a cada dato
        recetas_list = [{
            'id_receta':          r[0],
            'nombre_receta':      r[1],
            'valor_nutricional':  r[2],
            'nutriscore':         r[3] or 'C',  # Si viene vacío, pone 'C' por defecto
            'nombre_ingrediente': r[4],
            'sostenibilidad':     r[5],
            'celiaco':            r[6] or 0,    # Si viene vacío, pone 0 (no celíaco)
            'caducidad':          r[7],
            'fecha_creacion':     r[8],
        } for r in rows]

    except Exception as e:
        print("ERROR tus_recetas:", e)
        recetas_list = []  # Si algo falla, muestra la página con la lista vacía

    return render_template('tusrecetas.html', recetas=recetas_list)


@app.route('/receta/eliminar/<int:id_receta>', methods=['POST'])
def eliminar_receta(id_receta):
    # <int:id_receta> coge el número de la URL, por ejemplo /receta/eliminar/5
    if not session.get('id_cli'):
        return redirect('/login')

    id_cli = session['id_cli']
    try:
        cur = mysql.connection.cursor()
        # Comprueba que la receta pertenece al usuario antes de borrar nada
        cur.execute("SELECT id_receta FROM RECETA WHERE id_receta = %s AND id_cli = %s", (id_receta, id_cli))
        if not cur.fetchone():
            cur.close()
            return redirect('/tusrecetas')  # Si no es suya, redirige sin hacer nada

        # Borra primero los ingredientes de la receta y luego la receta en sí
        # (hay que borrar en ese orden porque RECETA_INGREDIENTE depende de RECETA)
        cur.execute("DELETE FROM RECETA_INGREDIENTE WHERE id_receta = %s", (id_receta,))
        cur.execute("DELETE FROM RECETA WHERE id_receta = %s AND id_cli = %s", (id_receta, id_cli))
        # GREATEST evita que num_recetas baje de 0 si por algún motivo ya estaba a 0
        cur.execute("UPDATE CLIENTE SET num_recetas = GREATEST(COALESCE(num_recetas,0)-1,0) WHERE id_cli = %s", (id_cli,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        mysql.connection.rollback()
        print("ERROR eliminar_receta:", e)

    return redirect('/tusrecetas')


@app.route('/pontureceta')
def pon_tu_receta():
    if not session.get('id_cli'):
        return redirect('/login')
    return render_template('pontureceta.html')


@app.route('/receta', methods=['POST'])
def receta():
    id_cli = session.get('id_cli')
    if not id_cli:
        return render_template('pontureceta.html', error_receta='Debes iniciar sesión para publicar una receta.')

    nombre_receta = request.form.get('nombre_receta', '').strip()
    nutriscore    = request.form.get('nutriscore', 'C')[0].upper()
    valor_raw     = request.form.get('valor_nutricional', '').strip()

    if not nombre_receta:
        return render_template('pontureceta.html', error_receta='El nombre de la receta es obligatorio.')

    # Convierte las calorías a número entero; si no es válido, devuelve error
    try:
        valor_nutricional = int(float(valor_raw)) if valor_raw else None
    except ValueError:
        return render_template('pontureceta.html', error_receta='El valor nutricional debe ser un número.')

    # getlist recoge varios valores del mismo campo (el formulario permite añadir
    # varios ingredientes, cada uno con su propio nombre, cantidad, etc.)
    nombres_ing    = request.form.getlist('nombre_ingrediente[]')
    cantidades     = request.form.getlist('cantidad[]')
    sostenibilidad = request.form.getlist('sostenibilidad_producto[]')
    cecliaco_list  = request.form.getlist('cecliaco[]')
    caducidad_list = request.form.getlist('caducidad[]')

    # Filtra los ingredientes vacíos
    ingredientes = [n.strip() for n in nombres_ing if n.strip()]
    if not ingredientes:
        return render_template('pontureceta.html', error_receta='Añade al menos un ingrediente.')

    try:
        cur = mysql.connection.cursor()
        # Guarda la receta principal
        cur.execute("""
            INSERT INTO RECETA (id_cli, nombre_receta, valor_nutricional, nutriscore)
            VALUES (%s, %s, %s, %s)
        """, (id_cli, nombre_receta[:50], valor_nutricional, nutriscore))
        id_receta = cur.lastrowid

        # Guarda cada ingrediente por separado y lo relaciona con la receta
        for idx, nombre_ing in enumerate(ingredientes):
            # Si el índice no llega, usa valores por defecto
            sost      = sostenibilidad[idx] if idx < len(sostenibilidad) else 'Nacional'
            celiaco   = int(cecliaco_list[idx]) if idx < len(cecliaco_list) else 0
            caducidad = caducidad_list[idx] if idx < len(caducidad_list) and caducidad_list[idx] else None

            cur.execute("""
                INSERT INTO INGREDIENTE (nombre_ingrediente, sostenibilidad_producto, cecliaco, caducidad)
                VALUES (%s, %s, %s, %s)
            """, (nombre_ing[:50], sost, celiaco, caducidad))
            # Relaciona el ingrediente recién insertado con la receta
            cur.execute("INSERT INTO RECETA_INGREDIENTE (id_receta, id_ingrediente) VALUES (%s, %s)", (id_receta, cur.lastrowid))

        cur.execute("UPDATE CLIENTE SET num_recetas = COALESCE(num_recetas, 0) + 1 WHERE id_cli = %s", (id_cli,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        mysql.connection.rollback()
        print("ERROR guardar receta:", e)
        return render_template('pontureceta.html', error_receta=f'Error al guardar: {e}')

    return redirect('/tusrecetas')


# Solo arranca el servidor si ejecutas este archivo directamente (no si lo importas desde otro)
if __name__ == '__main__':
    app.run(debug=True)  # debug=True recarga el servidor automáticamente al guardar cambios