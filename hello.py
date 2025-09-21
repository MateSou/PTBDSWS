from flask import Flask, render_template, url_for, session, redirect,flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
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

##Home Page
@app.route('/', methods=['POST', 'GET'])
def index():
    form = Form()
    if form.validate_on_submit():
        session['Name'] = form.name.data
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
           user = User(username=form.name.data)
           user.role_id = 3
           db.session.add(user)
           db.session.commit()
           session['known'] = False
        else:
            session['known'] = True
        return redirect(url_for('index'))
    return render_template('homepage.html', form=form, name=session.get('Name'), 
                           known=session.get('known'),users_list=User.query.all())


##Error 404 - Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html'), 404