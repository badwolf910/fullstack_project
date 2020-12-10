from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iqvgrzyaripdwl:01945a0bb98fc0f06e3f2ebd08d6a74c2e34c7a6cb45d9e8e7c2e1ac554b09cb@ec2-35-169-184-61.compute-1.amazonaws.com:5432/d3l1in65itk7d5'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    continent = db.Column(db.String(200))
    comments = db.Column(db.Text())

    def __init__(self, customer, continent, email, comments):
        self.customer = customer
        self.email = email
        self.continent = continent
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email = request.form['email']
        continent = request.form['continent']
        comments = request.form['comments']
        # print(customer, email, continent, comments)
        if customer == '' or continent == '':
            return render_template('form.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, continent, email, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, continent, email, comments)
            return render_template('success.html')
        return render_template('form.html', message='You have already submitted your idea')


if __name__ == '__main__':
    app.run()
