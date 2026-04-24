from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = 'MyNewPass1'   # ← pon la tuya
app.config['MYSQL_DB']       = 'jabali_db'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('RETO5.html')

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre   = request.form['nombre']
    email    = request.form['email']
    objetivo = request.form.get('objetivo', '')
    mensaje  = request.form.get('mensaje', '')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO contactos (nombre, email, objetivo, mensaje) VALUES (%s, %s, %s, %s)",
                (nombre, email, objetivo, mensaje))
    mysql.connection.commit()
    cur.close()

    return render_template('RETO5.html')
@app.route('/receta', methods=['POST'])
def receta():
    titulo      = request.form['titulo']
    categoria   = request.form.get('categoria', '')
    calorias    = request.form.get('calorias', '')
    proteina    = request.form.get('proteina', '')
    grasa       = request.form.get('grasa', '')
    ingredientes = request.form.get('ingredientes', '')
    preparacion = request.form.get('preparacion', '')

    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO recetas 
        (titulo, categoria, calorias, proteina, grasa, ingredientes, preparacion) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (titulo, categoria, calorias, proteina, grasa, ingredientes, preparacion))
    mysql.connection.commit()
    cur.close()

    return render_template('RETO5.html')

if __name__ == '__main__':
    app.run(debug=True)
