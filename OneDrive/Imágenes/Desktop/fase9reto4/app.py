from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from config import DB_CONFIG
import hashlib
from ia import sugerir_receta, generar_menu_semanal, analizar_nutriscore
#Ibon: Aqui importamos todo lo que hemos echo en la ia.py para poder usarlo en la aplicacion.
app = Flask(__name__)
app.secret_key = 'jabali_secret_key'
#Ibon: Esto es para configurar la conexion con la base de datos, lo que hemos echo en el config.py lo usamos aqui para conectar con la base de datos.
app.config['MYSQL_HOST']     = DB_CONFIG['host']
app.config['MYSQL_USER']     = DB_CONFIG['user']
app.config['MYSQL_PASSWORD'] = DB_CONFIG['password']
app.config['MYSQL_DB']       = DB_CONFIG['database']
app.config['MYSQL_CHARSET']  = 'utf8mb4'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('RETO5.html')

#Ibon: Esto te abre la parte de contacto
@app.route('/contacto', methods=['POST']) 
def contacto():
    # Ibon: Aqui lo que hacemos es poner el nombre y email, donde esta parte lo coge get('nombre', '').strip()
    nombre = request.form.get('nombre', '').strip()
    email  = request.form.get('email', '').strip()
    # Ibon: Si aqui no pones las dos te va a aparecer un error. Por eso se pone un error_contaco y esto lo vamos a encontrar muchas
    # Ibon: veces aqui en los codigos porque hay un monton de apartado donde hay que poner error_....
    if not nombre or not email:
        return render_template('RETO5.html', error_contacto='Nombre y email son obligatorios')
    # Con esto conectamos la pagina con la bases de datos con un mysql.connection.cursor()
    try:
        cur = mysql.connection.cursor()
        #Ibon:como hemos llamado cur a la connection ya no hace falta mas poner todo este codigo mysql.connection.cursor() y ponemos solo cur.
        #Ibon: el execute es para ejecutar el codigo.
        cur.execute("INSERT INTO USUARIO (nombre_usu, mail_usu) VALUES (%s, %s)", (nombre[:50], email))
        #Ibon: Para que se guarden los cambios sin el mysql.connection.commit() no guardaria
        mysql.connection.commit()
        #Ibon: cierra lo que hemos echo
        cur.close()
        #Ibon: Esto es si el codigo da bien te pondra Mensaje enviado. Te contactaremos pronto
        return render_template('RETO5.html', ok_contacto='Mensaje enviado. Te contactaremos pronto.')
    except Exception as e:
        #Ibon: Aqui ponemos except Exceptio as e por si da error cuando ejecutamos un codigo de bases para que nos avise.
        return render_template('RETO5.html', error_contacto=f'Error: {e}')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('registro.html')
    # Ibon: Es lo mismo que estoy haciendo en la de contacto. Aqui tambien se guardan los datos para meterlo a la bases de datos.
    nombre = request.form.get('nombre', '').strip()
    apellido1 = request.form.get('apellido1', '').strip()
    apellido2 = request.form.get('apellido2', '').strip()
    email = request.form.get('email', '').strip()
    telefono = request.form.get('telefono', '').strip()
    password = request.form.get('password', '')
    password2 = request.form.get('password2', '')
    
    # Ibon: Si no ponemso el nombre o apellido o email o contraseña automaticamente te da un error diciendo que los campos son obligatorios.
    if not nombre or not apellido1 or not email or not password:
        return render_template('registro.html', error='Rellena todos los campos obligatorios .')
    # Ibon: Aqui si la primera contraseña con coincide con la segunda tamben te va a dar error
    if password != password2:
        return render_template('registro.html', error='No coiciden las contraseñas.')
    #Ibon: Aqui es que si el telefono no es un numero entero no sirve y ponemos el except ValueError con un None de no saber
    try:
        telefono_int = int(telefono) if telefono else None
    except ValueError:
        telefono_int = None
    # Ibon: Para esta linea 75 hemos tenido que usar la ayuda de la IA para poder hacer que la contraseña no se vea si nos hackean. 
    # Ibon: Le llamamos pwd_hash y con el password.encode() hacemos que se convierta en bytes poruqe el sha256 solo trabajo con bytes.
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()[:200]
    # Lo mismo que antes lo conectamos con la base de datos y hacemos una consulta select
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_usu FROM USUARIO WHERE mail_usu = %s", (email,))
        # Ibon: Aqui elegimos el fetchone porque solo queremos una fila, si hubiera mas de un email igual no serviria
        if cur.fetchone():
            cur.close()
            #Este codigo daría
            return render_template('registro.html', error='Ese email ya está en uso.')
        #Consulta
        cur.execute("""
            INSERT INTO USUARIO (nombre_usu, apellido1_usu, apellido2_usu, mail_usu, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre[:50], apellido1[:50], apellido2[:50] or None, email, telefono_int))
        # Guardamos el id_usu recien creado antes de hacer otra consulta
        id_usu_nuevo = cur.lastrowid
        #Consulta
        cur.execute("""
            INSERT INTO CLIENTE (id_usu, num_logs, num_recetas, contrasenia) VALUES (%s, 0, 0, %s)
        """, (id_usu_nuevo, pwd_hash))
        #Ibon: Para que se guarden los cambios sin el mysql.connection.commit() no guardaria
        mysql.connection.commit()
        #Ibon: Cierre de la consulta
        cur.close()
        
    except Exception as e:
        #Ibon: Si da error al ejecutar el codigo de la base de datos, con el mysql.connection.rollback() hacemos que no se guarde nada de lo que se ha echo antes del error.
        mysql.connection.rollback()
        #Ibon: Y cauando nos de error nos va a aparecer el error
        return render_template('registro.html', error=f'Error al registrar: {e}')
    #Ibon: Pero si va todo bien, te va a dirigir automaticamente a login.
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # gahona: recoge el email y encripta la contraseña igual que al registrarse para poder compararlas
    email    = request.form.get('email', '').strip()
    pwd_hash = hashlib.sha256(request.form.get('password', '').encode()).hexdigest()[:200]

    try:
        cur = mysql.connection.cursor()
        # gahona: busca un usuario que su  email y contraseña coincidan en las dos tablas a la vez
        cur.execute("""
            SELECT u.id_usu, u.nombre_usu, c.id_cli
            FROM USUARIO u JOIN CLIENTE c ON u.id_usu = c.id_usu
            WHERE u.mail_usu = %s AND c.contrasenia = %s
        """, (email, pwd_hash))
        usuario = cur.fetchone()

        # gahona: si no encuentra ningún usuario con esos datos de usuario , muestra error
        if not usuario:
            cur.close()
            return render_template('login.html', error='Email o contraseña incorrectos.')

        # gahona: guarda los datos del usuario en la sesión para tenerlos disponibles la app
        session['id_usu'] = usuario[0]
        session['nombre'] = usuario[1]
        session['id_cli'] = usuario[2]

        # gahona: suma 1 al contador de logins; 
        # COALESCE evita errores si el campo era NULL
        cur.execute("UPDATE CLIENTE SET num_logs = COALESCE(num_logs, 0) + 1 WHERE id_cli = %s", (usuario[2],))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        return render_template('login.html', error=f'Error de conexión: {e}')

    return redirect('/')

#Ibon: Para cerrar la sesion
@app.route('/logout')
def logout():
    #Ibon: Esto es para cerrar la sesion y que no se pueda acceder a las paginas sin iniciar sesion
    session.clear()
    #Ibon: Te dirige a la pagina pricipal
    return redirect('/')


# gahona: solo pueden usar la IA los usuarios logueados
@app.route('/ia/sugerencia', methods=['POST'])
def ia_sugerencia():
    if not session.get('id_cli'):
        return redirect('/login')

    # gahona: recoge lo que el usuario ha escrito y se lo pasa a la función de IA
    ingrediente = request.form.get('ingrediente', '')
    nutriscore  = request.form.get('nutriscore', 'C')
    resultado   = sugerir_receta(ingrediente, nutriscore)

    # gahona: devuelve la página con la sugerencia generada y los datos del formulario
    # para que el usuario vea lo que había escrito junto con el resultado
    return render_template('RETO5.html',
        sugerencia_ia=resultado,
        ingrediente_ia=ingrediente,
        nutriscore_ia=nutriscore)


@app.route('/ia/guardar_receta', methods=['POST'])
def guardar_receta_ia():
    # gahona: verificar si el usuario esta logueado
    if not session.get('id_cli'):
        return redirect('/login')

    # gahona: [0].upper() coge solo la primera letra y la pone en mayúscula
    nombre_receta = request.form.get('nombre_receta', 'Receta IA')[:50]
    nutriscore    = request.form.get('nutriscore', 'C')[0].upper()
    id_cli        = session['id_cli']

    try:
        cur = mysql.connection.cursor()
        # gahona: crea un ingrediente genérico usando el nombre de la receta como nombre
        cur.execute("""
            INSERT INTO INGREDIENTE (nombre_ingrediente, sostenibilidad_producto, cecliaco)
            VALUES (%s, 'Nacional', 0)
        """, (nombre_receta,))
        #Ibon: Guardamos el id del ingrediente recien creado antes de hacer otra consulta
        id_ingrediente_nuevo = cur.lastrowid

        cur.execute("""
            INSERT INTO RECETA (id_cli, nombre_receta, nutriscore) VALUES (%s, %s, %s)
        """, (id_cli, nombre_receta, nutriscore))
        id_receta = cur.lastrowid

        # gahona: relaciona la receta con el ingrediente en la tabla intermedia
        cur.execute("INSERT INTO RECETA_INGREDIENTE (id_receta, id_ingrediente) VALUES (%s, %s)", (id_receta, id_ingrediente_nuevo))
        # gahona: suma 1 al contador de recetas del usuario
        cur.execute("UPDATE CLIENTE SET num_recetas = COALESCE(num_recetas, 0) + 1 WHERE id_cli = %s", (id_cli,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        # gahona: si algo falla deshace todos los cambios para no dejar datos a medias
        mysql.connection.rollback()
        return render_template('RETO5.html', error_receta=f'Error al guardar: {e}')

    return redirect('/tusrecetas')


@app.route('/ia/menu', methods=['POST'])
def ia_menu():
    # gahona: verificar si el usuario esta logueado
    if not session.get('id_cli'):
        return redirect('/login')

    preferencias = request.form.get('preferencias', 'equilibrada')
    menu = generar_menu_semanal(preferencias)
    return render_template('menu_semanal.html', menu_ia=menu)


# Ibon Etxegia

@app.route('/ia/analisis', methods=['POST'])
def ia_analisis():
    # Si no hay sesión activa, redirige al login
    if not session.get('id_cli'):
        return redirect('/login')
    # Recoge los datos del formulario
    nombre=request.form.get('nombre_receta', '')
    kcal=request.form.get('valor_nutricional', '0')
    score=request.form.get('nutriscore', 'C')
    # Llama a la función de análisis y devuelve el resultado
    analisis=analizar_nutriscore(nombre, kcal, score)
    return render_template('RETO5.html', analisis_ia=analisis)


@app.route('/receta', methods=['POST'])
def receta():
    #Ibon: Este codigo lo hacemos muchas veces para comprobar que el usuario ha iniciado sesion si no ha iniciado sesion no puedes entrar a la pagina
    id_cli = session.get('id_cli')
    if not id_cli:
        return render_template('pontureceta.html', error_receta='Debes iniciar sesión para publicar una receta.')

    # Verificamos que el id_cli de la sesion existe realmente en la base de datos
    # Si no existe (por ejemplo tras recrear las tablas) cerramos sesion y mandamos a login
    try:
        cur_check = mysql.connection.cursor()
        cur_check.execute("SELECT id_cli FROM CLIENTE WHERE id_cli = %s", (id_cli,))
        if not cur_check.fetchone():
            cur_check.close()
            session.clear()
            return redirect('/login')
        cur_check.close()
    except Exception as e:
        return render_template('pontureceta.html', error_receta=f'Error de sesión: {e}')

    nombre_receta = request.form.get('nombre_receta', '').strip()
    nutriscore    = request.form.get('nutriscore', 'C')[0].upper()
    valor_raw     = request.form.get('valor_nutricional', '').strip()

    if not nombre_receta:
        return render_template('pontureceta.html', error_receta='El nombre de la receta es obligatorio.')

    try:
        valor_nutricional = int(float(valor_raw)) if valor_raw else None
    except ValueError:
        return render_template('pontureceta.html', error_receta='El valor nutricional debe ser un número.')

    nombres_ing    = request.form.getlist('nombre_ingrediente[]')
    cantidades     = request.form.getlist('cantidad[]')
    sostenibilidad = request.form.getlist('sostenibilidad_producto[]')
    cecliaco_list  = request.form.getlist('cecliaco[]')
    caducidad_list = request.form.getlist('caducidad[]')

    ingredientes = [n.strip() for n in nombres_ing if n.strip()]
    if not ingredientes:
        return render_template('pontureceta.html', error_receta='Añade al menos un ingrediente.')

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO RECETA (id_cli, nombre_receta, valor_nutricional, nutriscore)
            VALUES (%s, %s, %s, %s)
        """, (id_cli, nombre_receta[:50], valor_nutricional, nutriscore))
        id_receta = cur.lastrowid

        for idx, nombre_ing in enumerate(ingredientes):
            sost      = sostenibilidad[idx] if idx < len(sostenibilidad) else 'Nacional'
            celiaco   = int(cecliaco_list[idx]) if idx < len(cecliaco_list) else 0
            caducidad = caducidad_list[idx] if idx < len(caducidad_list) and caducidad_list[idx] else None

            cur.execute("""
                INSERT INTO INGREDIENTE (nombre_ingrediente, sostenibilidad_producto, cecliaco, caducidad)
                VALUES (%s, %s, %s, %s)
            """, (nombre_ing[:50], sost, celiaco, caducidad))
            # Guardamos el id del ingrediente recien insertado antes de la siguiente consulta
            id_ingrediente_nuevo = cur.lastrowid
            cur.execute("INSERT INTO RECETA_INGREDIENTE (id_receta, id_ingrediente) VALUES (%s, %s)", (id_receta, id_ingrediente_nuevo))

        cur.execute("UPDATE CLIENTE SET num_recetas = COALESCE(num_recetas, 0) + 1 WHERE id_cli = %s", (id_cli,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        mysql.connection.rollback()
        print("ERROR guardar receta:", e)
        return render_template('pontureceta.html', error_receta=f'Error al guardar: {e}')

    return redirect('/tusrecetas')


if __name__ == '__main__':
    app.run(debug=True)
