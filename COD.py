from flask import Flask, redirect, url_for, render_template, request, session, flash
import requests
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///COD.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(40), nullable=False)
    email = db.Column('email', db.String(40),  nullable=False)
    password = db.Column('password', db.String(40), nullable=False)

    def __str__(self):
        return f'Cod username:{self.username}; email: {self.email}; password: {self.password}'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Cod.query.filter_by(username=username, password=password).first()

        if not user:
            session['username'] = username
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))

        else:
            session['username'] = username
            return redirect(url_for('stat'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('home.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/plays')
def plays():
    return render_template('plays.html')


@app.route('/stat', methods=['GET', 'POST'])
def stat():

    url = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone-matches/Amartin743/psn"

    headers = {
        "X-RapidAPI-Host": "call-of-duty-modern-warfare.p.rapidapi.com",
        "X-RapidAPI-Key": "ef9e4cf392msh28a220ad18b49ddp1197eejsn708559e6e8ff"
    }

    response = requests.request("GET", url, headers=headers)
    result_json = response.text
    resu = json.loads(result_json)

    m = resu['summary']
    all = m['all']
    kills = all['kills']
    death = all['deaths']
    asist = all['assists']

    kda = all['kdRatio']
    headsh = all['headshots']
    scor = all['score']

    return render_template('stat.html', kills=kills, death=death, asist=asist, kda=kda, headsh=headsh, scor=scor)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        u = request.form['username']
        e = request.form['email']
        p = request.form['password']
        user1 = Cod.query.filter_by(email=e).first()
        if user1:
            flash('Email address already exists')
            return render_template('registration.html')
        new_user = Cod(email=e, username=u, password=p)
        db.session.add(new_user)
        db.session.commit()

    return render_template('registration.html')


if __name__ == "__main__":
    app.run(debug=True)