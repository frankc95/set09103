from flask import Flask, render_template      
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
