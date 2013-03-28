from main import *
from flask import Flask, session, redirect, url_for, render_template
from flask.ext import login
from wtforms import Form, BooleanField, TextField, PasswordField, validators

app = Flask(__name__)

# login

# registration forms
class RegistrationForm(Form):
    email = TextField('Email Address')

@app.route("/")
def mainpage():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return "Register page"




if __name__ == "__main__":
    app.run(debug=True)


