from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange

# Forms
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterAccountForm(FlaskForm):
    fname = StringField("First Name:", validators=[DataRequired()])
    lname = StringField("Last Name:", validators=[DataRequired()])
    email = StringField("Email Address:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterPatientForm(FlaskForm):
    fname = StringField("First Name:", validators=[DataRequired()])
    lname = StringField("Last Name:", validators=[DataRequired()])
    insurance = StringField("Insurance Name:", validators=[DataRequired()])
    policy_num = IntegerField("Policy Number:", validators=[DataRequired()])
    phone = StringField("Phone Number:", validators=[DataRequired()])
    address = StringField("Address:", validators=[DataRequired()])
    econtact = StringField("Emergency Contact:", validators=[DataRequired()])
    econtact_phone = StringField("Emergency Contact Number:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PaymentForm(FlaskForm):
    payment_options = ["Credit Card", "Bank Transfer", "PayPal", "Cash"]
    payment_method = SelectField("Payment Method:", choices = payment_options, validators=[DataRequired()])
    pay_amount = FloatField("Payment Amount:", validators=[NumberRange(min=0)])
    submit = SubmitField("Submit Payment")