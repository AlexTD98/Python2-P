from distutils.log import warn
import re
from flask import Flask, render_template, request,redirect, url_for, flash, session
import urllib.request
import os
from flask_mysqldb import MySQL
import bcrypt
from werkzeug.utils import secure_filename
from flask_login import login_required


app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='alejandro'
app.config['MYSQL_DB']='pythonp'
app.config['UPLOAD_FOLDER'] = './static'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'
semilla = bcrypt.gensalt()


@app.route('/', methods=['GET','POST'])
def Index():
    if request.method == 'POST':
        return render_template('inicio.html')
    else: 
        return render_template('sesion.html')

@app.route('/Inicio',methods=['GET','POST'])
@login_required
def Inicio():
    if request.method == 'POST':
        nombre = request.form['keyword']
        cur = mysql.connection.cursor()
        qry = "SELECT * FROM pelis WHERE Nombre Like %s"
        cur.execute(qry,["%"+nombre+"%"])
        data = cur.fetchall()
        return render_template('inicio.html',peliculas=data)
    else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pelis')
        data = cur.fetchall()
        return render_template('inicio.html',peliculas=data)
    
@app.route('/inicio',methods=['GET','POST'])
@login_required
def inicio():
    if request.method == 'POST':
        nombre = request.form['keyword']
        cur = mysql.connection.cursor()
        qry = "SELECT * FROM pelis WHERE Nombre Like %s"
        cur.execute(qry,["%"+nombre+"%"])
        data = cur.fetchall()
        return render_template('inicioU.html',peliculas=data)
    else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pelis')
        data = cur.fetchall()
        return render_template('inicioU.html',peliculas=data)

@app.route('/INICIO',methods=['GET','POST'])
@login_required
def INICIO():
    if request.method == 'POST':
        nombre = request.form['keyword']
        cur = mysql.connection.cursor()
        qry = "SELECT * FROM pelis WHERE Nombre Like %s"
        cur.execute(qry,["%"+nombre+"%"])
        data = cur.fetchall()
        return render_template('inicioA.html',peliculas=data)
    else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pelis')
        data = cur.fetchall()
        return render_template('inicioA.html',peliculas=data)
    
@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if (request.method=="GET"):
        # Acceso denegado
        if 'nombre' in session:
            return render_template('inicio.html')
        else:
            return render_template('sesion.html')
    else:
        # Obtiene los datos de registro
        nombre = request.form['name']
        correo = request.form['email']
        password = request.form['password']
        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semilla)
        print("Insertado:")
        print("Password_encode: ", password_encode)
        print("Password_encriptado: ", password_encriptado)

        # Query para la inserción
        if len(nombre) == 0:
            flash("Ingresa el Nombre", "error")

            return render_template('sesion.html')
        else:
            sQuery = "INSERT into users(name, password, email,rol_id) VALUES ( %s, %s, %s,2)"
            # Crear cursor para ejecución
            cur = mysql.connection.cursor()

            # Ejecuta la sentencia
            cur.execute(sQuery,(nombre, password_encriptado, correo))

            # Ejecuta el commit
            mysql.connection.commit()

            # Registrar la sesión
            session['name'] = nombre
            session['email'] = correo

        # Redirigir a Index
        return redirect(url_for('inicio'))
    
@app.route("/ingresar", methods=["GET", "POST"])
def ingresar():
    if (request.method=="GET"):
        # Acceso denegado
        if 'nombre' in session:
            return render_template('inicio.html')
        else:
            return render_template('sesion.html')
    else:
        # Obtiene los datos de registro
        nombre = request.form['name']
        password = request.form['password']
        password_encode = password.encode("utf-8")
        password_decode = password_encode.decode('utf-8')

        # Crear cursor para ejecución
        cur = mysql.connection.cursor()

        # Query para consulta
        sQuery = "SELECT name, password, email, rol_id FROM users WHERE name = %s"
        
        # Ejecuta la sentencia
        cur.execute(sQuery,[nombre])
        
        # Obtener Dato
        usuario = cur.fetchone()
      
        # Cerrar consulta
        cur.close()

        # Verificar si se obtuvo el dato
        if (usuario != None):
            # Obtener el password encriptado
            password_encriptado_encode = usuario[1].encode()
            print("Password_encode: ", password_encode)
            print("Password_encriptado_encode: ", password_encriptado_encode)

            # Verificar el Password
            if (bcrypt.checkpw(password_encode,password_encriptado_encode)):
                # Registrar la sesión
                session['name'] = usuario[2]
                
                # Redirecciona a Index
                if (usuario[3]==3):
                    return redirect(url_for('Inicio'))
                elif (usuario[3]==1):
                    return redirect(url_for('INICIO'))
                elif (usuario[3]==2):
                    return redirect(url_for('inicio'))
            else:
                # Advertencia o Mensaje Flash
                flash("El Password Es Incorrecto", "alert-warning")

                # Redirigir a Ingresar
                return render_template('sesion.html')
        else:
            # Advertencia o Mensaje Flash
            flash("El Correo No Existe", "alert-warning")

            # Redirigir a Ingresar
            return render_template('sesion.html')
    

@app.route('/agregar')
def add_contact():
    return render_template('index.html')
@app.route('/recibir',methods=['POST'])
def recivir():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        año = request.form['año']
        genero = request.form['genero']
        duracion = request.form['duracion']
        idiomas = request.form['idiomas']
        portada = request.files['img']
        vid = request.form['link']
        filename = secure_filename(portada.filename)
        portada.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO pelis (Nombre,Descripcion,Año,Genero,Duracion,Idiomas,Img,Link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                    (nombre,descripcion,año,genero,duracion,idiomas,filename,vid))
        mysql.connection.commit()
        flash('Pelicula agregada correctamente')
        return redirect(url_for('inicio'))
    

@app.route('/Movie/<id>')
def Mostrar(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM pelis WHERE idPelis= %s',[id])
    data = cur.fetchall()
    return render_template('video.html',p_mo = data[0])

@app.route('/movie/<id>')
def mostrar(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM pelis WHERE idPelis= %s',[id])
    data = cur.fetchall()
    return render_template('videoU.html',p_mo = data[0])
    
    
@app.route('/editar')
def editar():
     cur = mysql.connection.cursor()
     cur.execute('SELECT * FROM pelis')
     data = cur.fetchall()
     return render_template('edit.html',peliculas=data)

@app.route('/edit/<id>')
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pelis WHERE idPelis= %s',[id])
    data = cur.fetchall()
    return render_template('edit_p.html',p_edi = data[0])

@app.route('/update/<id>',methods = ['POST'])
def update(id):
    if request.method == 'POST':
        Nombre = request.form['nombre']
        Descripcion = request.form['descripcion']
        Año = request.form['año']
        Genero = request.form['genero']
        Duracion = request.form['duracion']
        Idiomas = request.form['idiomas']
        portada = request.files['img']
        vid = request.form['link']
        filename = secure_filename(portada.filename)
        portada.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE pelis
        SET Nombre = %s,
            Descripcion = %s,
            Año = %s,
            Genero = %s,
            Duracion = %s,
            Idiomas = %s,
            Img = %s,
            Link = %s
        WHERE idPelis = %s
                    """,(Nombre,Descripcion,Año,Genero,Duracion,Idiomas,filename,vid,id))
        mysql.connection.commit()
        return redirect(url_for('inicio'))

@app.route('/delete/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pelis WHERE idPelis= {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('inicio'))

@app.route('/exit')
def exit():
    return redirect(url_for('Index'))

@app.route('/users')
def user():
    cur = mysql.connection.cursor()
    cur.execute('select name,email,rol from users us inner join roles rol on us.rol_id = rol.id where rol.id != 3')
    data = cur.fetchall()
    return render_template("users.html",users=data)

@app.route('/test')
def test():
    return render_template('F_Users.html')

if __name__ == '__main__':
    app.run(port = 3000,debug = True)