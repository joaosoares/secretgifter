from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, validators
from flask.ext.wtf import Required
from models import User

# FORM MODELS
# Login
class LoginForm(Form):
    email = TextField('Email', validators = [Required(), validators.Email()])
    password = PasswordField('Password', validators = [Required()])
    remember_me = BooleanField('Remember Me', default = False)

    def __init(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append('Unknown email')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True

# Registration
class RegistrationForm(Form):
    name = TextField('Your name', validators=[Required()])
    email = TextField('Email Address', validators=[Required(),validators.Email()])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.username.errors.append('Email already in use.')
            return False
        
        user = User(self.email.data, self.password.data, self.name.data)
        self.user = user
        return True



# Adding participants
class AddPersonForm(Form):
    name = TextField('Email Address')
    number = TextField('Number')
    gift = TextField('Gift')


