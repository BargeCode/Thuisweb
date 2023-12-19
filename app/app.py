from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, NamerForm, PasswordForm, PostForm, UserForm
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date


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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:geheim@mysql/gebruikers'
db = SQLAlchemy(app)

## Secret key
app.config['SECRET_KEY'] = "Avada kadabra"

## Webpages / Routes

# index page (homepage)
@app.route('/index')
def index():
    return render_template("index.html")

## Post stuff

# Posts (all)
@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts = posts)

# Post (single)
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post = post)

# Post Add page
@app.route('/posts/add-post', methods=['GET', 'POST'])
@login_required
def post_add():
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

    return render_template("post_add.html", form = form)

# Post Delete page
@app.route('/posts/delete/<int:id>')
@login_required
def post_delete(id):
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

# Edit post
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def post_edit(id):
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
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('post_edit.html', form = form)


## User stuff

# Users
@app.route('/user', methods=['GET', 'POST'])
@login_required
def users():
    gebruikers = Gebruikers.query.order_by(Gebruikers.id)
    return render_template(
        'users.html',
        gebruikers = gebruikers
    )

# User add route
@app.route('/user/add', methods=['GET', 'POST'])
def user_add():
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
        "user_add.html",
        form = form,
        name = name,
        gebruikers = gebruikers
        )

# User Dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    return render_template(
        'user_dashboard.html'
    )

# User Delete user
@app.route('/user/delete/<int:id>')
@login_required
def user_delete(id):
    user_to_delete = Gebruikers.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Verwijderd.")
        gebruikers = Gebruikers.query.order_by(Gebruikers.dates)
        return render_template(
        "user_add.html",
        form = form,
        name = name,
        gebruikers = gebruikers
        )
    except:
        flash("Woops. there it is.. verwijderen niet gelukt.")
        return render_template(
        "user_add.html",
        form = form,
        name = name,
        gebruikers = gebruikers
        )

# User Login page
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Gebruikers.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.pw_hash, form.password.data):
                login_user(user)
                flash("Ingelogd!")
                return redirect(url_for('user_dashboard'))
            else:
                flash("gebruiker/wachtwoord combi niet bekend")
        else: 
            flash("Gebruiker niet bekend, probeer opnieuw")
    return render_template(
        'user_login.html',
        form = form
    )

# User Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    flash('Je bent uitgelogd!')
    return redirect(url_for('user_login'))

# User Update page
@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
@login_required
def user_update(id):
    form = UserForm()
    name_to_update = Gebruikers.query.get_or_404(id)
    gebruikers = Gebruikers.query.order_by(Gebruikers.dates)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.favo_kl = request.form['favo_kl']
        try:
            db.session.commit()
            flash("Update succes!")
            return render_template(
                'user_update.html',
                form=form,
                name_to_update = name_to_update,
                id = id,
                gebruikers = gebruikers
                )
        except:
            flash("Wooooops.. iets ging niet goed.")
            return render_template(
                'user_update.html',
                form=form,
                name_to_update = name_to_update,
                id = id,
                gebruikers = gebruikers
                )
    else: 
        form.name.data = name_to_update.name
        form.username.data = name_to_update.username
        form.email.data = name_to_update.email
        form.favo_kl.data = name_to_update.favo_kl
        return render_template(
            'user_update.html',
            form=form,
            name_to_update = name_to_update,
            id = id,
            gebruikers = gebruikers
            )


## Others

# JSON route
@app.route('/date')
def get_current_date():
    return {'Date': date.today()}

# error pages #
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

    # 500 route
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


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
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
