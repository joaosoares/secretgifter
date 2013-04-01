import os
from app import app, db, lm
import main
from flask import jsonify, session, redirect, url_for, render_template, request, flash, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from forms import LoginForm, AddPersonForm, RegistrationForm
from models import User, Draw, Participant

@app.route("/")
def mainpage():
    if g.user.is_authenticated():
        recent_draws = Draw.query.filter_by(user_id=g.user.id).all()
        return render_template('dashboard.html', recent=recent_draws, user=current_user)
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
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
    logout_user()
    return redirect(url_for('mainpage'))

@app.route("/about/")
def about():
    print "Hi!"
    return render_template('about.html')

@app.route("/pricing/")
def pricing():
    return render_template('pricing.html')

@app.route("/draws/")
def draws():
    return "Draws"

@app.route("/draws/new/", methods=['GET', 'POST'])
@login_required
def new_draw():
    form = AddPersonForm()
    if form.validate_on_submit():
        # If there is data entered, make this a new draw
        new_draw = Draw(creator=g.user)
        db.session.add(new_draw)
        db.session.commit()
        # Add the participant
        new_person = Participant(name=form.name.data,
                number=form.number.data,
                gift=form.gift.data,
                draw_id=new_draw.id)
        db.session.add(new_person)
        db.session.commit()
        # Redirect to created draw
        return redirect(url_for('table', drawid=new_draw.id))
    return render_template("participants.html", form=form)

@app.route("/draws/<drawid>", methods = ['GET', 'POST'])
@login_required
def table(drawid):
    form = AddPersonForm()
    if form.validate_on_submit():
        new_person = Participant(name=form.name.data,
                number=form.number.data,
                gift=form.gift.data,
                draw_id=drawid)
        db.session.add(new_person)
        db.session.commit()
        participants = Participant.query.filter_by(draw_id=drawid).all()
        return render_template("participants.html", participants=participants, form=form)
    if g.user.id is not Draw.query.get(drawid).creator.id:
        return redirect(url_for('mainpage'))
    participants = Participant.query.filter_by(draw_id=drawid).all()
    return render_template("participants.html", participants=participants, form=form)

@app.route("/addcredits/")
def add_credits():
    return "Add credits"

@app.route("/account/")
def account():
    return "Account"

@app.before_request
def before_request():
    g.user = current_user

# Login Manager

@lm.unauthorized_handler
def unauthorized():
    return render_template('noauth.html')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

