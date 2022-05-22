from ctypes import create_unicode_buffer
from pickle import TRUE
from flask import Flask, render_template
from utils.db import db
from flask_sqlalchemy import SQLAlchemy
from models.models import login, student
from werkzeug.security import generate_password_hash
from crypt import methods
from click import password_option
from flask import Blueprint,render_template,request,redirect, url_for,flash
from models.models import logindb
from flask_login import current_user, login_required, login_user, logout_user


app = Flask(__name__)
app.secret_key = 'Ssdf3f34frdsa24352@@@'




app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:poiuy0mn@localhost/crud'
app.config[' SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SQLAlchemy(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
    
    

with app.app_context():
    db.create_all()

login.init_app(app)
login.login_view = 'login'

#ruta raiz
@app.route('/')
def index ():
    return redirect('login')

#ruta login
@app.route('/login',methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return 'logeado correctamente'
    
    if request.method == "POST":
         correo = request.form['email']
         usuario = logindb.query.filter_by(email = correo).first()
         if usuario is not None and usuario.check_password(usuario.password,request.form['password']):
             login_user(usuario)
             return 'logeado correctamente felicidades   '
         
    return render_template('login.html')

#ruta register
@app.route('/register', methods = ['GET','POST'])
def register():

    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        nombre_de_usuario = request.form['username']
        correo = request.form['email']
        password = request.form['password']

        if logindb.query.filter_by(email=correo).first():
            flash('Correo ya existente')
            return redirect('/register')

        clavesha = generate_password_hash(password)
        usuario = logindb(username=nombre_de_usuario,email=correo,password=clavesha)
        db.session.add(usuario)
        db.session.commit()

        return redirect('/login')
        
    return render_template('registro.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/crud')
@login_required
def home_crud():
   
    return 'pagina queva despues del login'


@app.route('/add', methods=['POST','GET'])
@login_required
def add():
    

    if request.method == 'POST':
       nombre = request.form['nombre']
       correo = request.form['correo']
       telefono = request.form['telefono']
       fecha_de_cumpleanos = request.form['fecha']
       students= student(nombre=nombre,correo=correo,telefono=telefono,fecha_de_cumpleanos=fecha_de_cumpleanos)
       db.session.add(students)
       db.session.commit()

       flash('Agregado correctamente')

       return redirect(url_for('crud.home_crud'))
    else:
        
        return render_template('add.html')


@app.route('/update/<id>', methods=['POST','GET'])
@login_required
def update(id):
    updateid = student.query.get(id)

    if request.method == 'POST':
       updateid.nombre = request.form['nombre']
       updateid.correo = request.form['correo']
       updateid.telefono = request.form['telefono']
       updateid.fecha_de_cumpleanos = request.form['fecha']
       db.session.commit()

       flash('Modificado correctamente')

       return redirect(url_for('crud.home_crud'))
    else:
        
        return render_template('update.html',updateid = updateid)


@app.route('/delete/<id>')
@login_required
def delete(id):
    deleteid =  student.query.get(id)
    db.session.delete(deleteid)
    db.session.commit()
    print(deleteid)
    flash('borrado correctamente')
    return redirect(url_for('crud.home_crud'))

@app.route('/about')
@login_required
def about():
   return render_template('about.html')




if __name__ == '__main__':
    app.run(debug=True)
