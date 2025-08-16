from flask import Flask, render_template 
from flask import request, make_response,redirect,abort
app = Flask(__name__)


##hello world
@app.route('/')
def index():
    return render_template('homepage.html')


##Dinamico
@app.route('/user/<name>/<pt>/<college>')
def user(name,pt,college):
    return render_template('identificacao.html', name=name,pt=pt,college=college) 

##Browser do usuario
@app.route('/contextorequisicao')
def browser():
    user_agent = request.headers.get('User-Agent')
    addr_client = request.remote_addr
    host = request.host
    return render_template('contexto_requisicao.html',
                           user_agent=user_agent,addr_client=addr_client,
                           host=host)

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
