#models application
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bop import db, login_manager, app
from flask_login import UserMixin

#decorate the function
@login_manager.user_loader
#user function that takes user as an argument
def load_user(user_id):
    #return user for that id
    return User.query.get(int(user_id))

#Class model table to hold user
class User(db.Model, UserMixin):
    #columns with conditions
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #relation to post - get author who created review
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return (("{first} {second} {third}").format(first=self.username, second=self.email, third=self.image_file))

#Class model that holds user Reviews
class Post(db.Model):
    #columns with conditions
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #relation to user - get id of the user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return (("{first} {second}").format(first=self.title, second=self.date_posted))

