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
        flash("Welcome!")
        return redirect(url_for('mainpage'))
    return render_template('login.html', form = form)

@app.route("/register")
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.email.data, form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/about/")
def about():
    return "About page"

@app.route("/pricing/")
def pricing():
    return "Pricing page"

@app.route("/draws/<drawid>", methods = ['GET', 'POST'])
def table(drawid):
    add_form = AddPersonForm()
    if add_form.validate_on_submit():
        pass
    return render_template("participants.html", form=add_form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
