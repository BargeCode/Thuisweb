from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, equal_to, Length
from flask import Flask, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_wtf import FlaskForm



# Create a flask instance
app = Flask(__name__)
app.app_context().push()

# App config
## Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gebruikers.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:geheim@mysql/gebruikers'
db = SQLAlchemy(app)

## Secret key
app.config['SECRET_KEY'] = "Avada kadabra"

# Classes #
    # Database
class Gebruikers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favo_kl = db.Column(db.String(120))
    dates = db.Column(db.DateTime, default=datetime.utcnow)
    pw_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name

    # Ask user details page
class UserForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favo_kl = StringField("Favoriete kleur")
    pw_hash = PasswordField(
        "Wachtwoord",
        validators=[DataRequired(),
                    equal_to('pw_hash2',
                             message='Wachtwoorden moeten overeenkomen!')])
    pw_hash2 = PasswordField("Herhaal wachtwoord", validators=[DataRequired()])
    submit = SubmitField("Opslaan") 

    # Ask-name page
class NamerForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired()])
    submit = SubmitField("Verstuur")
class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    pw_hash = PasswordField("Wachtwoord", validators=[DataRequired()])
    submit = SubmitField("Verstuur")

# JSON route
@app.route('/date')
def get_current_date():
    return {'Date': date.today()}


# index route
@app.route('/index')
def index():
    return render_template("index.html")

# add user route
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Gebruikers.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.pw_hash.data, "sha256")
            user = Gebruikers(
                name=form.name.data,
                email=form.email.data,
                favo_kl=form.favo_kl.data,
                pw_hash=hashed_pw
            )
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favo_kl.data = ''
        form.pw_hash.data = ''
        form.pw_hash2.data = ''
        flash("Gebruiker toegevoegd")
    gebruikers = Gebruikers.query.order_by(Gebruikers.dates)
    return render_template(
        "add_user.html",
        form = form,
        name = name,
        gebruikers = gebruikers
        )

# Change DB record route
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Gebruikers.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favo_kl = request.form['favo_kl']
        try:
            db.session.commit()
            flash("Update succes!")
            return render_template(
                'update.html',
                form=form,
                name_to_update = name_to_update
                )
        except:
            flash("Wooooops.. iets ging niet goed.")
            return render_template(
                'update.html',
                form=form,
                name_to_update = name_to_update
                )
    else: 
        return render_template(
            'update.html',
            form=form,
            name_to_update = name_to_update,
            id = id
            )

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Gebruikers.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Verwijderd.")
        gebruikers = Gebruikers.query.order_by(Gebruikers.dates)
        return render_template(
        "add_user.html",
        form = form,
        name = name,
        gebruikers = gebruikers
        )
    except:
        flash("Woops. there it is.. verwijderen niet gelukt.")
        return render_template(
        "add_user.html",
        form = form,
        name = name,
        gebruikers = gebruikers
        )


# user route
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name_=name)

# name route
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Form validation
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('je naam is verstuurd!')

    return render_template(
        "name.html",
        name = name,
        form = form)

# test pw route
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    user_to_check = None
    passed = None
    form = PasswordForm()
    
    # Form validation
    if form.validate_on_submit():
        email = form.email.data
        password = form.pw_hash.data
        form.email.data = ''
        form.pw_hash.data = ''
        user_to_check = Gebruikers.query.filter_by(email=email).first()
        passed = check_password_hash(pwhash=user_to_check.pw_hash, password=password)



    return render_template(
        "test_pw.html",
        email = email,
        password = password,
        user_to_check = user_to_check,
        form = form,
        passed = passed
    )


# error pages #
    # 404 route
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

    # 500 route
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
