from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField,StringField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar de Mim')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
        'Usernames must have only letters, numbers, dots or '
        'underscores')])
    password = PasswordField('Senha', validators=[DataRequired(), EqualTo('password2', message='As Senhas devem ser iguais')])
    password2 = PasswordField('Confime a senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Este e-mail já foi registrado')
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Este username já foi registrado.')
        
class ChangePassowordForm(FlaskForm):
    old_password = PasswordField('Senha antiga', validators=[DataRequired()])
    new_password = PasswordField('Nova Senha', validators=[DataRequired(),EqualTo('new_password2', message='As senhas devem ser iguais')])
    new_password2 = PasswordField('Confirme a senha', validators=[DataRequired()])
    submit = SubmitField('Atualizar Senha')

class ChangeEmailForm(FlaskForm):
    new_email = EmailField('Novo E-mail', validators=[DataRequired(),Length(1,64), Email()])
    passoword = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Mudar E-mail')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Este e-mail já está registrado')
        
class RequestToResetPassword(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(1,64), Email()])
    submit = SubmitField('Resetar Senha')

class ResetPassword(FlaskForm):
    new_password = PasswordField('Nova senha', validators=[DataRequired(), Length(1,64), EqualTo('confirm_password', message='As senhas devem ser iguais')])
    confirm_password = PasswordField('Confirme a senha', validators=[DataRequired()])
    submit = SubmitField('Trocar a senha')