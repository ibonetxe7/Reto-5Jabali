# -*- coding: utf-8 -*-
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


# ─── INDEX ───────────────────────────────────
@app.route('/')
def index():
    return render_template('RETO5.html')


# ─── CONTACTO ────────────────────────────────
@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre', '').strip()
    email  = request.form.get('email', '').strip()

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


# ─── PON TU RECETA ───────────────────────────
@app.route('/receta', methods=['POST'])
def receta():
    id_cli = session.get('id_cli')
    if not id_cli:
        return render_template('RETO5.html', error_receta='Debes iniciar sesion antes de publicar una receta.')

    nombre_receta      = request.form.get('nombre_receta', '').strip()
    nombre_ingrediente = request.form.get('nombre_ingrediente', '').strip()
    nutriscore         = request.form.get('nutriscore', 'C')[0].upper()
    sostenibilidad     = request.form.get('sostenibilidad_producto', 'Nacional')
    cecliaco           = int(request.form.get('cecliaco', '0'))
    caducidad          = request.form.get('caducidad') or None
    valor_raw          = request.form.get('valor_nutricional', '').strip()

    if not nombre_receta:
        return render_template('RETO5.html', error_receta='El nombre de la receta es obligatorio.')
    if not nombre_ingrediente:
        return render_template('RETO5.html', error_receta='El ingrediente principal es obligatorio.')

    try:
        valor_nutricional = int(float(valor_raw)) if valor_raw else None
    except ValueError:
        return render_template('RETO5.html', error_receta='El valor nutricional debe ser un numero.')

    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO INGREDIENTE (nombre_ingrediente, sostenibilidad_producto, cecliaco, caducidad)
            VALUES (%s, %s, %s, %s)
        """, (nombre_ingrediente[:50], sostenibilidad, cecliaco, caducidad))
        id_ingrediente = cur.lastrowid

        cur.execute("""
            INSERT INTO RECETA (id_cli, nombre_receta, valor_nutricional, nutriscore)
            VALUES (%s, %s, %s, %s)
        """, (id_cli, nombre_receta[:50], valor_nutricional, nutriscore))
        id_receta = cur.lastrowid

        cur.execute("""
            INSERT INTO RECETA_INGREDIENTE (id_receta, id_ingrediente) VALUES (%s, %s)
        """, (id_receta, id_ingrediente))

        cur.execute("UPDATE CLIENTE SET num_recetas = COALESCE(num_recetas, 0) + 1 WHERE id_cli = %s", (id_cli,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        mysql.connection.rollback()
        return render_template('RETO5.html', error_receta=f'Error al guardar: {e}')

    return render_template('RETO5.html', ok_receta='Receta guardada correctamente.')


# ─── REGISTRO ────────────────────────────────
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

        try:
            telefono_int = int(telefono) if telefono else None
        except ValueError:
            telefono_int = None

        password_hash = hashlib.sha256(password.encode()).hexdigest()[:200]

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id_usu FROM USUARIO WHERE mail_usu = %s", (email,))
            if cur.fetchone():
                cur.close()
                return render_template('registro.html', error='El email ya esta registrado.')

            cur.execute("""
                INSERT INTO USUARIO (nombre_usu, apellido1_usu, apellido2_usu, mail_usu, telefono)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre[:50], apellido1[:50], apellido2[:50] if apellido2 else None, email, telefono_int))
            id_usu = cur.lastrowid

            cur.execute("""
                INSERT INTO CLIENTE (id_usu, num_logs, num_recetas, contrasenia) VALUES (%s, 0, 0, %s)
            """, (id_usu, password_hash))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            mysql.connection.rollback()
            return render_template('registro.html', error=f'Error al registrar: {e}')

        return redirect('/login')

    return render_template('registro.html')


# ─── LOGIN ───────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email         = request.form.get('email', '').strip()
        password_hash = hashlib.sha256(request.form.get('password', '').encode()).hexdigest()[:200]

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT u.id_usu, u.nombre_usu, c.id_cli
                FROM USUARIO u JOIN CLIENTE c ON u.id_usu = c.id_usu
                WHERE u.mail_usu = %s AND c.contrasenia = %s
            """, (email, password_hash))
            usuario = cur.fetchone()

            if not usuario:
                cur.close()
                return render_template('login.html', error='Email o contrasena incorrectos.')

            session['id_usu'] = usuario[0]
            session['nombre'] = usuario[1]
            session['id_cli'] = usuario[2]

            cur.execute("UPDATE CLIENTE SET num_logs = COALESCE(num_logs, 0) + 1 WHERE id_cli = %s", (usuario[2],))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            return render_template('login.html', error=f'Error de conexion: {e}')

        return redirect('/')

    return render_template('login.html')


# ─── LOGOUT ──────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ─── IA SUGERENCIA ───────────────────────────
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
        nutriscore_ia=nutriscore
    )


# ─── IA GUARDAR RECETA ───────────────────────
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
        id_ingrediente = cur.lastrowid

        cur.execute("""
            INSERT INTO RECETA (id_cli, nombre_receta, nutriscore)
            VALUES (%s, %s, %s)
        """, (id_cli, nombre_receta, nutriscore))
        id_receta = cur.lastrowid

        cur.execute("""
            INSERT INTO RECETA_INGREDIENTE (id_receta, id_ingrediente) VALUES (%s, %s)
        """, (id_receta, id_ingrediente))

        cur.execute("UPDATE CLIENTE SET num_recetas = COALESCE(num_recetas, 0) + 1 WHERE id_cli = %s", (id_cli,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        mysql.connection.rollback()
        return render_template('RETO5.html', error_receta=f'Error al guardar: {e}')

    return render_template('RETO5.html', ok_receta='✅ Receta de la IA guardada correctamente.')


# ─── IA MENU SEMANAL ─────────────────────────
@app.route('/ia/menu', methods=['POST'])
def ia_menu():
    if not session.get('id_cli'):
        return redirect('/login')
    preferencias = request.form.get('preferencias', 'equilibrada')
    menu         = generar_menu_semanal(preferencias)
    return render_template('menu_semanal.html', menu_ia=menu)


# ─── IA ANALISIS ─────────────────────────────
@app.route('/ia/analisis', methods=['POST'])
def ia_analisis():
    if not session.get('id_cli'):
        return redirect('/login')
    nombre   = request.form.get('nombre_receta', '')
    kcal     = request.form.get('valor_nutricional', '0')
    score    = request.form.get('nutriscore', 'C')
    analisis = analizar_nutriscore(nombre, kcal, score)
    return render_template('RETO5.html', analisis_ia=analisis)


if __name__ == '__main__':
    app.run(debug=True)