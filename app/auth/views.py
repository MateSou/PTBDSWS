from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, ResetPassword, RegistrationForm, ChangePassowordForm, ChangeEmailForm,RequestToResetPassword
from app import db
from ..emails import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Email ou Senha errado')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()  
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Cadastro feito. Você pode entrar na sua conta agora.')
        flash('Um e-mail foi enviado para você confirmar sua conta')
        token = user.generate_confirmation_token()
        send_email(user.email,'CONFIRME SUA CONTA',render_template('auth/email/confirm_account.html',user=user,token=token))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/update-password', methods=['GET', 'POST'])
@login_required
def updatePassword():
    form = ChangePassowordForm()
    if form.validate_on_submit():
        user = User.load_user(current_user.get_id())
        if user.verify_password(form.old_password.data) is False: #Verifica se a senha atual está correta
            flash('Esta não é a sua senha atual')
            return redirect(url_for('auth.updatePassword'))
        user.password = form.new_password.data
        db.session.commit()
        flash('Sua senha foi atualizada')
        return redirect(url_for('main.index'))
    return render_template('auth/changePassword.html',form=form)

@auth.route('/update-email', methods=['GET', 'POST'])
@login_required
def updateEmail():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        user = User.load_user(current_user.get_id())
        if user.verify_password(form.passoword.data) is False:
            flash('Senha Errada')
            return redirect(url_for('.updateEmail'))
        if User.query.filter_by(email=form.new_email.data).first():
            flash('Este e-mail já foi cadastrado')
            return redirect(url_for('.updateEmail'))
        user.email = form.new_email.data
        user.confirmed = False
        db.session.commit()
        token = user.generate_confirmation_token()
        flash('Enviamos um novo e-mail com instruções para confirmar seu novo endereço de e-mail')
        flash('Para confirmar seu novo endereço de email <a href="' + url_for('.confirmEmail', token=token, _external=True) + '">clique aqui</a>')
        return redirect(url_for('main.index'))
    return render_template('auth/changeEmail.html', form=form)

@auth.route('confirm/login/<token>')
@login_required
def confirmEmail(token):
    user = User.load_user(current_user.get_id())
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Email Confirmado com sucesso.')
    else:
        flash('Link inválido ou expirado')
    return redirect(url_for('main.index'))

@auth.route('/reset-password', methods=['GET', 'POST'])
def resetPassword():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = RequestToResetPassword()
    if form.validate_on_submit():  
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Este e-mail não existe')
            return redirect(url_for('.resetPassword'))
        flash('Enviamos um e-mail com instruções para redefinir sua senha')
        token = user.generate_reset_token()
        send_email(user.email, 'REDEFINA SUA SENHA', render_template('auth/email/reset_password.html',user=user, token=token))
        return redirect(url_for('.login'))
    return render_template('auth/changePassword.html', form=form)

@auth.route('/confirm/password/<token>', methods=['GET', 'POST'])
def confirmPassword(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPassword()
    if form.validate_on_submit():
        if User.reset_password(token,form.new_password.data) is False:
            flash('Algo deu errado :( . Sentimos muito!')
            return redirect(url_for('main.index'))
        db.session.commit()
        flash('Senha resetada. Agora você pode fazer login')
        return redirect(url_for(('.login')))
    return render_template('auth/changePassword.html', form=form)
    
