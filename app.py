import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'sqlite:///feedback.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.debug = os.environ.get('FLASK_DEBUG', '').lower() in {'1', 'true', 'yes'}
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    continent = db.Column(db.String(200))
    comments = db.Column(db.Text())

    def __init__(self, customer, email, continent, comments):
        self.customer = customer
        self.email = email
        self.continent = continent
        self.comments = comments


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form')
def form():
    return render_template("form.html")


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form.get('customer', '').strip()
        email = request.form.get('email', '').strip()
        continent = request.form.get('continent', '').strip()
        comments = request.form.get('comments', '').strip()
        # print(customer, email, continent, comments)
        if customer == '' or continent == '':
            return render_template('form.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, email, continent, comments)
            db.session.add(data)
            db.session.commit()

            return render_template('success.html')
        return render_template('success.html')


if __name__ == '__main__':
    app.run()
