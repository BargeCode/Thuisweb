from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, equal_to, Length
from flask_sqlalchemy import SQLAlchemy
from wtforms.widgets import TextArea
from datetime import datetime, date
from flask_wtf import FlaskForm



# Create a flask instance
app = Flask(__name__)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Gebruikers.query.get(int(user_id))

# App config
## Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gebruikers.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:geheim@mysql/gebruikers'
db = SQLAlchemy(app)

## Secret key
app.config['SECRET_KEY'] = "Avada kadabra"

# Classes #
# Database
class Gebruikers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False, unique = True)
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
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
# Forms
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

    # Ask-name page
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
class LoginForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators = [DataRequired()])
    password = PasswordField("Wachtwoord", validators = [DataRequired()])
    submit = SubmitField("versturen")

# JSON route
@app.route('/date')
def get_current_date():
    return {'Date': date.today()}

# index route (homepage)
@app.route('/index')
def index():
    return render_template("index.html")

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Gebruikers.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.pw_hash, form.password.data):
                login_user(user)
                flash("ingelogd!")
                return redirect(url_for('dashboard'))
            else:
                flash("gebruiker/wachtwoord combi niet bekend")
        else: 
            flash("Gebruiker niet bekend, probeer opnieuw")
    return render_template(
        'login.html',
        form = form
    )

# Logout page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user
    flash('Je bent uitgelogd!')
    return redirect(url_for('login'))

# Dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template(
        'dashboard.html'
    )

# Add user route
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
                username = form.username.data,
                email=form.email.data,
                favo_kl=form.favo_kl.data,
                pw_hash=hashed_pw
            )
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
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

# Update user
@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Gebruikers.query.get_or_404(id)
    gebruikers = Gebruikers.query.order_by(Gebruikers.dates)
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
                name_to_update = name_to_update,
                id = id,
                gebruikers = gebruikers
                )
        except:
            flash("Wooooops.. iets ging niet goed.")
            return render_template(
                'update.html',
                form=form,
                name_to_update = name_to_update,
                id = id,
                gebruikers = gebruikers
                )
    else: 
        form.name.data = name_to_update.name
        form.email.data = name_to_update.email
        form.favo_kl.data = name_to_update.favo_kl
        return render_template(
            'update.html',
            form=form,
            name_to_update = name_to_update,
            id = id,
            gebruikers = gebruikers
            )

# Delete user
@app.route('/user/delete/<int:id>')
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

# All posts
@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts = posts)

# Specific post
@app.route('/posts/<int:id>')
def blog_post(id):
    post = Posts.query.get_or_404(id)
    return render_template("blog_post.html", post = post)

# Add post route
@app.route('/posts/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(
            title = form.title.data,
            content = form.content.data,
            author = form.author.data,
            slug = form.slug.data
        )
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit()
        flash('Posted!')

    return render_template("add_post.html", form = form)

# Edit post
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Updated")
        return redirect(url_for('blog_post', id=post.id))
    
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form = form)

# Delete post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Bericht verwijderd.")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts = posts)
    except:
        flash("Whoopsie, er is een probleem opgetreden met het verwijderen van het bericht.")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts = posts)

# depricated. (user/name)
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name_=name)

# depricated. (name)
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

# error pages #
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

    # 500 route
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
