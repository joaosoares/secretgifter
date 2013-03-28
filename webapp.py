import os
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

@app.route("/about")
def about():
    return "About page"

@app.route("/pricing")
def pricing():
    return "Pricing page"

@app.route("/table")
def table():
    return render_template("participants.html")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


