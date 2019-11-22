import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

#secret_key protects against modyfing cookies, Cross-Site Request Forgery attack, etc
app.secret_key = '\xe3\x03\xc7\xa9\x9a\xd7\xfe\xf7\x12\xe1\xc2##D\xa4R\xcf\x9e\xb3\x96}s\xd8\x99'
app.config['SECRET_KEY'] = '\xe3\x03\xc7\xa9\x9a\xd7\xfe\xf7\x12\xe1\xc2##D\xa4R\xcf\x9e\xb3\x96}s\xd8\x99'
#location of database. Sqlite is a file in a file system.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#pass app as an argument to bd
db = SQLAlchemy(app)
#pass app an an argument to bcrypt
bcrypt = Bcrypt(app)
#instance of a login manager
login_manager = LoginManager(app)
#set the login route and set to login
login_manager.login_view = 'login'
#flash message within login manager and set to Bootstrap class 'info'
login_manager.login_message_category = 'info'
#set email server
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#set email port number
app.config['MAIL_PORT'] = '587'
#set
app.config['MAIL_USE_TLS'] = 'True'
app.config['MAIL_USERNAME'] = 'blazewicz.j@gmail.com'
app.config['MAIL_PASSWORD'] = 'ruralistyka12-18-6'
mail = Mail(app)



from bop import routes
