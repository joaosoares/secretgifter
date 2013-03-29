import os
from app import app, db, lm
import main
from flask import session, redirect, url_for, render_template, request, flash, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from forms import LoginForm, AddPersonForm, RegistrationForm
import models

@app.route("/")
def mainpage():
    if g.user.is_authenticated():
        return "Youre logged in bro"
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('mainpage'))
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
        db.session.add(form.user)
        db.session.commit()
        login_user(form.user)
        return redirect(url_for('mainpage'))
    return render_template('register.html', form=form)

@app.route('/logout/')
def logout():
    logodut_user()
    return redurect(url_for('mainpage'))

@app.route("/about/")
def about():
    print "Hi!"
    return "About page"

@app.route("/pricing/")
def pricing():
    return render_template('pricing.html')

@app.route("/draws/new/")
def new_draw():
    # IN FUTURE CHECK FOR AUTH AND STUFF
    new_draw = models.Draw()
    db.session.add(new_draw)
    db.session.commit()
    print "New draw created..."
    print new_draw.id
    return redirect(url_for('table', drawid=new_draw.id))

    

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

