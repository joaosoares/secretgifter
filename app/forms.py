from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, validators
from flask.ext.wtf import Required

# FORM MODELS
# Login
class LoginForm(Form):
    email = TextField('Email', validators = [Required()])
    password = PasswordField('Password', validators = [Required()])
    remember_me = BooleanField('Remember Me', default = False)

# Registration
class RegistrationForm(Form):
    email = TextField('Email Address')
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

# Adding participants
class AddPersonForm(Form):
    name = TextField('Email Address')
    number = TextField('Number')
    gift = TextField('Gift')


