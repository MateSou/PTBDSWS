from flask import Flask, render_template,url_for
from flask import request, make_response,redirect,abort
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

##hello world
@app.route('/')
def index():
    return render_template('homepage.html',current_time=datetime.utcnow())


##Dinamico
@app.route('/user/<name>/<prontuario>/<instituicao>')
def user(name,prontuario,instituicao):
    return render_template('identificacao.html', name=name,
                           prontuario=prontuario, instituicao=instituicao)

##Browser do usuario
@app.route('/contextorequisicao/<name>')
def browser(name):
    user_agent = request.headers.get('User-Agent')
    addr_client = request.remote_addr
    host = request.host
    return render_template('contexto_requisicao.html',
                           user_agent=user_agent,addr_client=addr_client,
                           host=host, name=name)

##Object response 
@app.route('/objetoresposta')
def objresp():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

##bad request 
@app.route ('/codigostatusdiferente')
def cod():
    return '<p>Bad request</p>', 400

##redirecionamento
@app.route ('/redirecionamento')
def redir():
    return redirect('https://ptb.ifsp.edu.br/')

##Abortar
@app.route('/abortar')
def abortar():
    abort (404)    

##Error 404 - Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html'), 404