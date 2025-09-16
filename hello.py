from flask import Flask, render_template, url_for, session, redirect,flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'senhasecreta'
moment = Moment(app)


#Uma funcao que possui uma lista de opcoes de disciplinas
def ListaDisciplinas():
    disciplinas_lista = [('DSWA5', 'DSWA5'), ('DWBA4', 'DWBA4'), ('GestaoDeProjetos', 
                                                                  'Gestão de Projetos')]
    return disciplinas_lista


class NameForm(FlaskForm):
    #Campo do formulario para inserir o nome. equivalente a 
    # <input type='text'>
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    last_name = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    instituicao_ensino = StringField('Informe a sua instituição de ensino:', 
                                     validators=[DataRequired()])
    disciplina  = SelectField('Informe a sua disciplina:',choices=ListaDisciplinas())
    #Campo do formulario para enviar os dados. equivalente a 
    # <input type='submit'>
    submit = SubmitField('Enviar')

class LoginForm(FlaskForm):
    #dicionario de dicionarios com atributos dos campos do formulario
    field_attributes= {
        "user_name_or_email": {'placeholder':'Usuário ou e-mail', 'class':'panel-body'},
        "user_secret": {'placeholder':'Informe a sua senha', 'class':'panel-body'},
        "submit": {'class':'btn btn-primary'}
    }
    
    #Nome ou email
    user_name_or_email = StringField('Login:',validators=[DataRequired()],id='user-name-email',
                                     render_kw=field_attributes['user_name_or_email'])
    #Senha
    user_secret = PasswordField(' ',validators=[DataRequired()],id='user-passwd', 
                                render_kw=field_attributes['user_secret'])
    #Submit
    submit = SubmitField('Enviar', id='submit-button',render_kw=field_attributes['submit'])


##Home Page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    remote_addr = request.remote_addr
    host = request.host
    #Dicionário que contém as informacoes do usuario para serem passados ao render_template
    user_infos = {
        "name": session.get('name'),
        "lastName": session.get('lastName'),
        "instituicaoDeEnsino": session.get('instituicao'),
        "disciplina": session.get('disciplina')
    }
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Você alterou o seu nome!')
        session['name'] = form.name.data
        session['lastName'] = form.last_name.data
        session['instituicao'] = form.instituicao_ensino.data
        session['disciplina'] = form.disciplina.data

        return redirect(url_for('index'))
    
    return render_template('homepage.html',form=form,user=user_infos,remote_addr=remote_addr,
                           host=host,current_time=datetime.utcnow())

##Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_infos = {
        'nameOrEmail':form.user_name_or_email.data,
        'secret':form.user_secret.data
    }
    if form.validate_on_submit():
        session['userLogin'] = user_infos.get('nameOrEmail')
        return redirect(url_for('loginResponse'))

    return render_template('login.html',form=form,current_time=datetime.utcnow())

##Login Response
#Funcao que apenas renderiza a pagina do resultado do Login
@app.route('/loginResponse')
def loginResponse():
    return render_template('loginResponse.html',name=session.get('userLogin'),current_time=datetime.utcnow())

##Error 404 - Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html'), 404