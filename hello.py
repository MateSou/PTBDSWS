from flask import Flask, render_template, url_for, session, redirect
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import requests
import os 
import datetime


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app,db)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'senhasecreta'

app.config['API_KEY'] = os.getenv('API_KEY')
app.config['API_URL'] = os.getenv('API_URL')
app.config['API_FROM'] = os.getenv('API_FROM')
app.config['FLASK_MAIL_SUBJECT_PREFIX'] = '[Flask]'
app.config['FLASK_ADMIN'] = os.getenv('FLASK_ADMIN')
app.config['EMAIL_PROF'] = os.getenv('EMAIL_PROF')


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
    email = db.relationship('Email', backref='user', uselist=False)

class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True, index=True)
    destination = db.Column(db.String(64))
    subject = db.Column(db.String(64))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

## Formularios
class Form(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    send_email = BooleanField("Deseja enviar e-mail para flaskaulasweb@zohomail.com?", "")
    submit = SubmitField('Enviar')

## E-mail
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
           if form.send_email.data:
               if app.config['FLASK_ADMIN']:
                   send_email([app.config['FLASK_ADMIN'],app.config['EMAIL_PROF']],'Novo Usuário',
                              form.name.data)
               email_destination = str(app.config['FLASK_ADMIN'] + ', ' + app.config['EMAIL_PROF'])
               email_subject = app.config['FLASK_MAIL_SUBJECT_PREFIX'] + ' - '+ 'Novo Usuário'
               email_body = "Novo usuário cadastrado.\n" + "Nome: " + str(form.name.data) + "\n" + "\nAluno: " + str(os.getenv('NOME')) + "\nPRONTUARIO: " + str(os.getenv('PRONTUARIO'))
               email_date = datetime.datetime.now().replace(microsecond=0)
               email = Email(destination=email_destination,subject=email_subject,text=email_body,date=email_date,user_id = user.id)
               db.session.add(email)
               db.session.commit()                              
        else:
            session['known'] = True
        return redirect(url_for('index'))
    
    return render_template('homepage.html', form=form, name=session.get('Name'), 
                           known=session.get('known', False),users = User.query.all(), emails = Email.query.all())

@app.route('/emailsEnviados')
def emailsEnviados():
    return render_template('emails.html', emails=Email.query.all())


##Error 404 - Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html'), 404