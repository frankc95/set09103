import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort, send_from_directory
from bop import app, db, bcrypt, mail
from bop.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm, ContactForm
from bop.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message, Mail


#@app.route is a decorator that handles backend and allows to write a function that returns information that will be showned on the website with this specific route
@app.route("/")
@app.route("/home")
#def is a function name
def home():
    return render_template('home.html', active='home')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'denger')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender=form.email.data, recipients=['blazewicz.napier@gmail.com'])
            msg.body = '''
            From: %s
            At: %s

            %s
            ''' % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            flash('Your message has been sent. We will reply to you shortly', 'success')
            return render_template('contact.html', form=form)
    elif request.method == 'GET':
        return render_template('contact.html', title='Contact', form=form, active='contact')


@app.route("/gallery")
def gallery():
    #creates space for an arrey
    albums = []
    album_paths = []
    album_image = []
    #foreach subdir in dir 'galleries'
    for root in os.walk('./bop/static/img/galleries/'):
        #list all subdirs and files
        albums.append(root)
    #foreach index in legth albums    
    for index in range(len(albums)):
        #list all and split into individual paths and show last path '[-1]'
        album_paths.append(albums[index][0].split('/')[-1])
    album_image.append(albums[1][2][1])
    
    print album_image[0] 
    
    return render_template('gallery.html', title='Gallery', active='gallery', albums=album_paths, album_image=album_image, album_paths=album_paths)

@app.route("/album/")
@app.route("/album/<album_path>")
def album(album_path):
    #if empty
    if album_path == False:
        #redirect to gallery
        return redirect(url_for('gallery'))
    #otherwise
    else:
        #loop through dir and specific subdir
        image_names = os.listdir('./bop/static/img/galleries/' + album_path)
        #open album.html and display content of specific subdir
        return render_template('album.html', title='Albums', active='gallery', image_names=image_names, album_path=album_path)


@app.route("/resources")
def resources():
    return render_template('resources.html', title='Resources', active='resources')

@app.route("/review")
def review():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('review.html', title='Reviews', posts=posts, active='review')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    #if form validated on submit
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        #flash message in flask is an easy way to display one time allert
        flash('Your account has been created! You are now able to log in', 'success')
        #return redirect takes user to login after registration if form validates properly
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, active='register')

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
    return render_template('login.html', title='Login', form=form, active='login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile_pic', picture_fn)
    
    output_size = (120, 100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/profile_pic/' + current_user.image_file)
    return render_template('account.html', title='account', image_file=image_file, form=form, active='account')


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your review has been created', 'success')
        return redirect(url_for('review'))
    return render_template('create_review.html', title='New Review', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your review has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_review.html', title='Update Review', form=form, legend='Update Review')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your review has been deleted', 'success')
    return redirect(url_for('review'))


@app.route("/user/<string:username>")
def user_review(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_reviews.html', posts=posts, user=user)

