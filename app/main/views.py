from datetime import datetime 
from flask import render_template, session, redirect, url_for
from . import main
from .forms import Form
from .. import db
from ..models import User
from ..emails import send_email
from config import Config

@main.route('/', methods=['GET', 'POST'])
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
           admin_email = Config.FLASK_ADMIN
           prof_email = Config.EMAIL_PROF
           user_email = form.user_email.data
           if admin_email:
               send_email([admin_email, prof_email, user_email],'Novo Usuário',
                              form.name.data)
        else:
            session['known'] = True
        return redirect(url_for('.index'))
    return render_template('homepage.html')