from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from utils.db import db

login = LoginManager()


class logindb(UserMixin,db.Model):
    
    __tablename__ = 'users'

    id= db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100))
    email= db.Column(db.String(100),unique=True)
    password= db.Column(db.String(102), nullable=False)


    def check_password(self,password_hash,password):
        return check_password_hash(password_hash,password) 
        

@login.user_loader
def load_user(id):
    return logindb.query.get(int(id))


#esta tabla dejala siquieres colocar el crud xd despues del login
class student(db.Model):

    __tablename__ = 'student'
    id= db.Column(db.Integer,primary_key=True)
    nombre =db.Column(db.String(50))
    correo = db.Column(db.String(100))
    telefono = db.Column(db.Integer)
    

    def __init__(self,nombre,correo,telefono,fecha_de_cumpleanos):
        self.nombre = nombre
        self.correo = correo
        self.telefono =telefono





   
