import ConfigParser

from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '\xe3\x03\xc7\xa9\x9a\xd7\xfe\xf7\x12\xe1\xc2##D\xa4R\xcf\x9e\xb3\x96}s\xd8\x99'

app.secret_key = '\xe3\x03\xc7\xa9\x9a\xd7\xfe\xf7\x12\xe1\xc2##D\xa4R\xcf\x9e\xb3\x96}s\xd8\x99'

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/config/')
def config():
    str = []
    str.append('Debug:'+app.config['DEBUG'])
    str.append('port:'+app.config['port'])
    str.append('url:'+app.config['url'])
    str.append('ip_address:'+app.config['ip_address'])
    return '\t'.join(str)

def init(app):
    config = ConfigParser.ConfigParser()
    try:
        config_location = "etc/defaults.cfg"
        config.read(config_location)

        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")
    except:
        print "Could not read configs from:, config_location"

        init(app)

if __name__ == '__main__':
    init(app)
    app.run(
            host=app.config['ip_address'],
            port=int(app.config['port']))
