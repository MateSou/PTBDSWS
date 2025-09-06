from flask import Flask, render_template, url_for, session, redirect,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'senhasecreta'

class NameForm(FlaskForm):
    #Campo do formulario para inserir o nome. equivalente a 
    # <input type='text'>
    name = StringField('What is your name?', validators=[DataRequired()])
    #Campo do formulario para enviar os dados. equivalente a 
    # <input type='submit'>
    submit = SubmitField('Submit')

##hello world
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect (url_for('index'))
    return render_template('homepage.html',form=form,name = session.get('name'))

##Error 404 - Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html'), 404