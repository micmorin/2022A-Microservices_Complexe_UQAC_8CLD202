from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,  EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField('Submit')

class User():
    c_user = None

    def __init__(self, id, name, username, email, token, profil):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.profil = profil
        self.token = token

        
    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False     

    def get_id(self):
        return str(self.token)   

    def get(user_id):
        return User.c_user

