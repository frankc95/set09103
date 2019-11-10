from flask import  render_template, flash, redirect, url_for, request
from bop import app, db, bcrypt
from bop.forms import RegistrationForm, LoginForm
from bop.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Jakub Blazewicz',
        'title': 'Blog',
        'content': 'frist post content',
        'date_posted': 'November 1st, 2019'
     },
    {
        'author': 'Aleksander Blazewicz',
        'title': 'Bloger',
        'content': 'second post content',
        'date_posted': 'November 31st, 2019'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')

@app.route("/gallery")
def gallery():
    return render_template('gallery.html', title='Gallery')

@app.route("/resources")
def resources():
    return render_template('resources.html', title='Resources')

@app.route("/review")
def review():
    return render_template('review.html', title='Reviews', posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='account')

