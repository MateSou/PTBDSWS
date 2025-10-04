from flask import Flask, render_template, url_for, session, redirect
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import requests
import os 


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'senhasecreta'

app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['API_URL'] = os.environ.get('API_URL')
app.config['API_FROM'] = os.environ.get('API_FROM')
app.config['FLASK_MAIL_SUBJECT_PREFIX'] = '[Flask]'
app.config['FLASK_ADMIN'] = os.environ.get('FLASK_ADMIN')


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
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    submit = SubmitField('Enviar')

def send_email(to,subject,newUser): 
        email_from = app.config['API_FROM']
        email_text = "Novo usuário cadastrado.\n" + "Nome: " + str(newUser) + "\n" + "\nAluno: " + str(os.getenv('NOME')) + "\nPRONTUARIO: " + str(os.getenv('PRONTUARIO'))
        return requests.post(
            app.config['API_URL'],
            auth=("api", app.config['API_KEY']),
            data={"from": email_from,
                  "to":to,
                "subject":app.config['FLASK_MAIL_SUBJECT_PREFIX'] + ' - '+ subject,
                "text":email_text})
    

##Home Page
@app.route('/', methods=['POST', 'GET'])
def index():
    form = Form()
    if form.validate_on_submit():
        #Salvando os dados enviado na sessão
        session['Name'] = form.name.data
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
           user = User(username=form.name.data,role_id=3)
           db.session.add(user)
           db.session.commit()
           session['known'] = False
           if app.config['FLASK_ADMIN']:
               send_email([app.config['FLASK_ADMIN'],"flaskaulasweb@zohomail.com"], 
                          'Novo Usuário', 
                          form.name.data)
        else:
            session['known'] = True
        return redirect(url_for('index'))
    
    return render_template('homepage.html', form=form, name=session.get('Name'), 
                           known=session.get('known', False))

##Error 404 - Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html'), 404