# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from config import DB_CONFIG
import hashlib

app = Flask(__name__)
app.secret_key = 'jabali_secret_key'

app.config['MYSQL_HOST']     = DB_CONFIG['host']
app.config['MYSQL_USER']     = DB_CONFIG['user']
app.config['MYSQL_PASSWORD'] = DB_CONFIG['password']
app.config['MYSQL_DB']       = DB_CONFIG['database']
app.config['MYSQL_CHARSET']  = 'utf8mb4'

mysql = MySQL(app)


# ─────────────────────────────────────────────
#  INDEX
# ─────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('RETO5.html')


# ─────────────────────────────────────────────
#  CONTACTO
# ─────────────────────────────────────────────
@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre', '').strip()
    email  = request.form.get('email',  '').strip()

    if not nombre or not email:
        return render_template('RETO5.html', error_contacto='Nombre y email son obligatorios.')

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO USUARIO (nombre_usu, mail_usu) VALUES (%s, %s)", (nombre[:50], email))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        return render_template('RETO5.html', error_contacto=f'Error: {e}')

    return render_template('RETO5.html', ok_contacto='Mensaje enviado. Te contactaremos pronto.')


# ─────────────────────────────────────────────
#  PON TU RECETA
# ─────────────────────────────────────────────
@app.route('/receta', methods=['POST'])
def receta():
    print("=" * 50)
    print("FORM:", dict(request.form))
    print("SESSION:", dict(session))
    print("=" * 50)

    id_cli = session.get('id_cli')

    if not id_cli:
        return render_template('RETO5.html',
            error_receta='Debes iniciar sesion antes de publicar una receta.')

    nombre_receta      = request.form.get('nombre_receta', '').strip()
    valor_raw          = request.form.get('valor_nutricional', '').strip()
    nutriscore         = request.form.get('nutriscore', 'C').strip()
    nombre_ingrediente = request.form.get('nombre_ingrediente', '').strip()
    sostenibilidad     = request.form.get('sostenibilidad_producto', 'Nacional').strip()
    cecliaco           = request.form.get('cecliaco', '0').strip()
    caducidad          = request.form.get('caducidad') or None

    if not nombre_receta:
        return render_template('RETO5.html', error_receta='El nombre de la receta es obligatorio.')
    if not nombre_ingrediente:
        return render_template('RETO5.html', error_receta='El ingrediente principal es obligatorio.')

    try:
        valor_nutricional = int(float(valor_raw)) if valor_raw else None
    except ValueError:
        return render_template('RETO5.html', error_receta='El valor nutricional debe ser un numero.')

    nutriscore = nutriscore[0].upper() if nutriscore else 'C'

    try:
        cur = mysql.connection.cursor()

        cur.execute("SELECT id_cli FROM CLIENTE WHERE id_cli = %s", (id_cli,))
        if not cur.fetchone():
            cur.close()
            session.clear()
            return render_template('RETO5.html',
                error_receta='Tu sesion no es valida. Vuelve a iniciar sesion.')

        cur.execute("""
            INSERT INTO INGREDIENTE (nombre_ingrediente, sostenibilidad_producto, cecliaco, caducidad)
            VALUES (%s, %s, %s, %s)
        """, (nombre_ingrediente[:50], sostenibilidad, int(cecliaco), caducidad))
        id_ingrediente = cur.lastrowid

        cur.execute("""
            INSERT INTO RECETA (id_ingrediente, id_cli, nombre_receta, valor_nutricional, nutriscore)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_ingrediente, id_cli, nombre_receta[:50], valor_nutricional, nutriscore))

        cur.execute("""
            UPDATE CLIENTE SET num_recetas = COALESCE(num_recetas, 0) + 1 WHERE id_cli = %s
        """, (id_cli,))

        mysql.connection.commit()
        cur.close()
        print("COMMIT OK")

    except Exception as e:
        mysql.connection.rollback()
        print(f"ERROR: {e}")
        return render_template('RETO5.html', error_receta=f'Error al guardar: {e}')

    return render_template('RETO5.html', ok_receta='Receta guardada correctamente.')


# ─────────────────────────────────────────────
#  REGISTRO — ahora guarda nombre, apellido1,
#  apellido2, email, telefono y password (en localidad)
# ─────────────────────────────────────────────
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre    = request.form.get('nombre', '').strip()
        apellido1 = request.form.get('apellido1', '').strip()
        apellido2 = request.form.get('apellido2', '').strip()
        email     = request.form.get('email', '').strip()
        telefono  = request.form.get('telefono', '').strip()
        password  = request.form.get('password', '')
        password2 = request.form.get('password2', '')

        if not nombre or not apellido1 or not email or not password:
            return render_template('registro.html', error='Los campos obligatorios (*) son necesarios.')

        if password != password2:
            return render_template('registro.html', error='Las contrasenas no coinciden.')

        # Convertir teléfono a int si viene, si no None
        try:
            telefono_int = int(telefono) if telefono else None
        except ValueError:
            telefono_int = None

        # Hash SHA256 recortado a 50 chars (localidad VARCHAR(50))
        password_hash = hashlib.sha256(password.encode()).hexdigest()[:50]

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id_usu FROM USUARIO WHERE mail_usu = %s", (email,))
            if cur.fetchone():
                cur.close()
                return render_template('registro.html', error='El email ya esta registrado.')

            cur.execute("""
                INSERT INTO USUARIO (nombre_usu, apellido1_usu, apellido2_usu, mail_usu, telefono, localidad)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                nombre[:50],
                apellido1[:50],
                apellido2[:50] if apellido2 else None,
                email,
                telefono_int,
                password_hash
            ))
            id_usu = cur.lastrowid

            cur.execute("""
                INSERT INTO CLIENTE (id_usu, num_logs, num_recetas) VALUES (%s, 0, 0)
            """, (id_usu,))

            mysql.connection.commit()
            cur.close()

        except Exception as e:
            mysql.connection.rollback()
            return render_template('registro.html', error=f'Error al registrar: {e}')

        return redirect('/login')

    return render_template('registro.html')


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_hash = hashlib.sha256(password.encode()).hexdigest()[:50]

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT u.id_usu, u.nombre_usu, c.id_cli
                FROM USUARIO u
                JOIN CLIENTE c ON u.id_usu = c.id_usu
                WHERE u.mail_usu = %s AND u.localidad = %s
            """, (email, password_hash))
            usuario = cur.fetchone()

            if not usuario:
                cur.close()
                return render_template('login.html', error='Email o contrasena incorrectos.')

            session['id_usu'] = usuario[0]
            session['nombre'] = usuario[1]
            session['id_cli'] = usuario[2]

            cur.execute("""
                UPDATE CLIENTE SET num_logs = COALESCE(num_logs, 0) + 1 WHERE id_cli = %s
            """, (usuario[2],))
            mysql.connection.commit()
            cur.close()

        except Exception as e:
            return render_template('login.html', error=f'Error de conexion: {e}')

        return redirect('/')

    return render_template('login.html')


# ─────────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)