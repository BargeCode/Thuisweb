from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, equal_to, Length
from wtforms.widgets import TextArea
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators = [DataRequired()])
    password = PasswordField("Wachtwoord", validators = [DataRequired()])
    submit = SubmitField("versturen")

class NamerForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired()])
    submit = SubmitField("Verstuur")

class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    pw_hash = PasswordField("Wachtwoord", validators=[DataRequired()])
    submit = SubmitField("Verstuur")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired()])
    username = StringField("Gebruikersnaam", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favo_kl = StringField("Favoriete kleur")
    pw_hash = PasswordField(
        "Wachtwoord",
        validators=[DataRequired(),
                    equal_to('pw_hash2',
                             message='Wachtwoorden moeten overeenkomen!')])
    pw_hash2 = PasswordField("Herhaal wachtwoord", validators=[DataRequired()])
    submit = SubmitField("Opslaan") 