from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = '\xe3\x03\xc7\xa9\x9a\xd7\xfe\xf7\x12\xe1\xc2##D\xa4R\xcf\x9e\xb3\x96}s\xd8\x99'
app.config['SECRET_KEY'] = '\xe3\x03\xc7\xa9\x9a\xd7\xfe\xf7\x12\xe1\xc2##D\xa4R\xcf\x9e\xb3\x96}s\xd8\x99'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from bop import routes
