from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField, DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User,Inventory

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class InventoryRemove(FlaskForm):
    item_code = IntegerField('Item Code', validators=[DataRequired()])
    submit = SubmitField('Remove')

    def validate_item_code(self, item_code):
        item = Inventory.query.filter_by(id=item_code.data).first()
        if item is None:
            raise ValidationError('this is not a valid code')
        if not isinstance(item_code.data,int):
            raise ValidationError('this needs to be a whole number')

class InventoryAdd(FlaskForm):
    source = StringField('Source', validators=[DataRequired()])
    name = StringField('Item Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Add')