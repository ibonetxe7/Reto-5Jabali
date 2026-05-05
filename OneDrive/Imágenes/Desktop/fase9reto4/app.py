from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from config import DB_CONFIG
import hashlib
from ia import sugerir_receta, generar_menu_semanal, analizar_nutriscore

app = Flask(__name__)
app.secret_key = 'jabali_secret_key'

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
    password2 = request.form.get('password', '')
    
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
        #Consulta
        cur.execute("""
            INSERT INTO CLIENTE (id_usu, num_logs, num_recetas, contrasenia) VALUES (%s, 0, 0, %s)
        """, (cur.lastrowid, pwd_hash))
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

    email    = request.form.get('email', '').strip()
    pwd_hash = hashlib.sha256(request.form.get('password', '').encode()).hexdigest()[:200]

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT u.id_usu, u.nombre_usu, c.id_cli
            FROM USUARIO u JOIN CLIENTE c ON u.id_usu = c.id_usu
            WHERE u.mail_usu = %s AND c.contrasenia = %s
        """, (email, pwd_hash))
        usuario = cur.fetchone()

        if not usuario:
            cur.close()
            return render_template('login.html', error='Email o contraseña incorrectos.')

        session['id_usu'] = usuario[0]
        session['nombre'] = usuario[1]
        session['id_cli'] = usuario[2]

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


@app.route('/ia/sugerencia', methods=['POST'])
def ia_sugerencia():
    if not session.get('id_cli'):
        return redirect('/login')

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
    nutriscore    = request.form.get('nutriscore', 'C')[0].upper()
    id_cli        = session['id_cli']

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO INGREDIENTE (nombre_ingrediente, sostenibilidad_producto, cecliaco)
            VALUES (%s, 'Nacional', 0)
        """, (nombre_receta,))

        cur.execute("""
            INSERT INTO RECETA (id_cli, nombre_receta, nutriscore) VALUES (%s, %s, %s)
        """, (id_cli, nombre_receta, nutriscore))
        id_receta = cur.lastrowid

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

    preferencias = request.form.get('preferencias', 'equilibrada')
    menu = generar_menu_semanal(preferencias)
    return render_template('menu_semanal.html', menu_ia=menu)


@app.route('/ia/analisis', methods=['POST'])
def ia_analisis():
    if not session.get('id_cli'):
        return redirect('/login')

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

        recetas_list = [{
            'id_receta':          r[0],
            'nombre_receta':      r[1],
            'valor_nutricional':  r[2],
            'nutriscore':         r[3] or 'C',
            'nombre_ingrediente': r[4],
            'sostenibilidad':     r[5],
            'celiaco':            r[6] or 0,
            'caducidad':          r[7],
            'fecha_creacion':     r[8],
        } for r in rows]

    except Exception as e:
        print("ERROR tus_recetas:", e)
        recetas_list = []

    return render_template('tusrecetas.html', recetas=recetas_list)


@app.route('/receta/eliminar/<int:id_receta>', methods=['POST'])
def eliminar_receta(id_receta):
    if not session.get('id_cli'):
        return redirect('/login')

    id_cli = session['id_cli']
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id_receta FROM RECETA WHERE id_receta = %s AND id_cli = %s", (id_receta, id_cli))
        if not cur.fetchone():
            cur.close()
            return redirect('/tusrecetas')

        cur.execute("DELETE FROM RECETA_INGREDIENTE WHERE id_receta = %s", (id_receta,))
        cur.execute("DELETE FROM RECETA WHERE id_receta = %s AND id_cli = %s", (id_receta, id_cli))
        cur.execute("UPDATE CLIENTE SET num_recetas = GREATEST(COALESCE(num_recetas,0)-1,0) WHERE id_cli = %s", (id_cli,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        mysql.connection.rollback()
        print("ERROR eliminar_receta:", e)

    return redirect('/tusrecetas')


@app.route('/pontureceta')
def pon_tu_receta():
    # Ibon: isto es que si no has iniciado sesion no puedes acceder a esta pagina y te redirige a login
    if not session.get('id_cli'):
        return redirect('/login')
    #Ibon: Si va bien te va a abrir la pagina pontureceta.html
    return render_template('pontureceta.html')


@app.route('/receta', methods=['POST'])
def receta():
    #Ibon: Este codigo lo hacemos muchas veces para comprobar que el usuario ha iniciado sesion si no ha iniciado sesion no puedes entrar a la pagina
    id_cli = session.get('id_cli')
    if not id_cli:
        return render_template('pontureceta.html', error_receta='Debes iniciar sesión para publicar una receta.')

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
            cur.execute("INSERT INTO RECETA_INGREDIENTE (id_receta, id_ingrediente) VALUES (%s, %s)", (id_receta, cur.lastrowid))

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
