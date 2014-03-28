from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, SelectField, PasswordField, validators
from wtforms import ValidationError
from models import Subscriber
from configobj import ConfigObj


# config data
config = ConfigObj('config_settings.ini')
admin_password = (config['admin_password']['password'])


class AddSubscriber(Form):
	username = TextField('Username', [validators.Required('You must supply a username')])
	password = PasswordField('Password', [validators.Required("You must supply a password")])
	adminpassword = PasswordField('Administrator password', [validators.Required('You must supply an administrator password')])
	submit = SubmitField('Create user account')

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		if self.adminpassword.data == self.get_admin_password():
			user = Subscriber.query.filter_by(username = self.username.data.lower()).first()
			if user:
				self.username.errors.append('That username is in use. Try again.')
				return False
			else:
				return True
		else:
			self.adminpassword.errors.append('Invalid administrator password')
			return False

	def get_admin_password(self):
		return admin_password