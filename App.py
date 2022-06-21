from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import CSRFProtect
from config import config

from models.ModelUser import ModelUser
from models.entities.User import User


app = Flask(__name__)

db = MySQL(app)
login_manager_app = LoginManager(app)
csrf = CSRFProtect()

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        user = User(0, request.form['username'],request.form['password'])
        logged_user = ModelUser.login(db,user)

        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('inicio'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User Not Found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/inicio',methods=['GET','POST'])
#Proteger pagina
@login_required
def inicio():
    if request.method == 'POST':
        nombre = request.form['keyword']
        cur = db.connection.cursor()
        qry = "SELECT * FROM pelis WHERE Nombre Like %s"
        cur.execute(qry,["%"+nombre+"%"])
        data = cur.fetchall()
        return render_template('inicio.html',peliculas=data)
    else:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM pelis')
        data = cur.fetchall()
        return render_template('inicio.html',peliculas=data)

#def status_401(error):
    return redirect(url_for('login'))

#def status_404(error):
    return "Page not found! ", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    csrf.init_app(app)
    #app.register_error_handler(401,status_401)
    #app.register_error_handler(404,status_404)
    app.run()