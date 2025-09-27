from flask import Flask, render_template, url_for, session, redirect
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import os 


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'senhasecreta'

migrate = Migrate(app, db)

##Banco de Dados
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
     #relacionamento um-para-muitos com users
    users = db.relationship('User', backref='role', lazy='dynamic')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

## Formularios
class Form(FlaskForm):
    choices = [('Moderator', 'Moderator'), ('User', 'User'), ('Administrator', 'Administrator')]
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    role = SelectField('Role', choices=choices)
    submit = SubmitField('Enviar')

##Home Page
@app.route('/', methods=['POST', 'GET'])
def index():
    form = Form()
    if form.validate_on_submit():
        session['Name'] = form.name.data
        session['Role'] = form.role.data
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
           #role pode ser um objeto do tipo Role, que é o role (papel) selecionado pelo user
           role = Role.query.filter_by(name=form.role.data).first()
           user = User(username=form.name.data,role=role)
           db.session.add(user)
           db.session.commit()
           #Salvando os dados enviado na sessão
           session['known'] = False
        else:
            session['known'] = True
        return redirect(url_for('index'))
    
    #Lista de todos os usuários cadastrados
    users_list=User.query.all()
    #quantidade de usuários cadastrados
    quantidade_users_cadastrados = len(users_list)
    #quantidade de funções cadastradas
    quantidade_roles_cadastradas = len(Role.query.all())
    #Dicionário de listas de usuários com determinado papel
    users_role = {
        'administrator': User.query.filter_by(role_id=1).all(),
        'moderator': User.query.filter_by(role_id=2).all(),
        'user': User.query.filter_by(role_id=3).all()
    }
    return render_template('homepage.html', form=form, name=session.get('Name'), 
                           known=session.get('known'),users_quantidade=quantidade_users_cadastrados,
                           users_list=users_list,roles_quantidade=quantidade_roles_cadastradas,
                           users_role=users_role)


##Error 404 - Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html'), 404