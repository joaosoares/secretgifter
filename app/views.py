import os
from app import app, db, lm
from main import *
from flask import session, redirect, url_for, render_template, request, flash, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from forms import LoginForm, AddPersonForm, RegistrationForm
from models import User

@app.route("/")
def mainpage():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    #if g.user is not None and g.user.is_authenticated():
    #    return redirect(url_for('mainpage'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        login_user(form.user)
        flash("Welcome, %s!" % form.user.name)
        return redirect(url_for('mainpage'))
    if form.errors:
        flash("Incorrect user or password")
    return render_template('login.html', form = form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Thanks for registering. You have been logged in.')
        login_user(form.user)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redurect(url_for('mainpage'))

@app.route("/about/")
def about():
    return "About page"

@app.route("/pricing/")
def pricing():
    return render_template('pricing.html')

@app.route("/draws/<drawid>", methods = ['GET', 'POST'])
def table(drawid):
    add_form = AddPersonForm()
    if add_form.validate_on_submit():
        pass
    return render_template("participants.html", form=add_form)

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

