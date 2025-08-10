from flask import Flask 
from flask import request, make_response,redirect,abort
app = Flask(__name__)


##hello world
@app.route('/')
def index():
    return '<h1>Hello World!</h1> <h2>Disciplina PTBDSWS</h2>'


##Dinamico
@app.route('/user/<name>')
def user(name):
    return '<h1>Ola, {}!</h1>'.format(name) 

##Browser do usuario
@app.route('/contextorequisicao')
def browser():
    user_agent = request.headers.get('User-Agent')
    return '<p>Seu navegador é {}</p>'.format(user_agent)

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

@app.route('/abortar')
def abortar():
    abort (404)
    

    



