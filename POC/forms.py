from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length, EqualTo, Email
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField

class FeedbackForm(FlaskForm):
    name = StringField("Name")
    contact = IntegerField("Mobile", validators= [DataRequired("Contact Required!!!!")])
    email = StringField("Email",validators=[DataRequired("Email Required!!"),Email("Provide a valid Email Address!!")])
    address = TextAreaField("Address", validators=[DataRequired("Required Field")])
    city = StringField("City")
    areaofinterest = StringField("Area of Interest",validators=[DataRequired("Required!!!")])
    feedback = TextAreaField("Feedback", validators=[DataRequired("Required Field")], description="Enter feeback here.....")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired("Required")])
    password = PasswordField("Password",validators=[DataRequired("Required")])
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired("Username Required!!")])
    email = StringField("Email",validators=[DataRequired("Email Required!!"),Email("Provide a valid Email Address!!")])
    mobile = IntegerField("Mobile",validators=[DataRequired("Contact Required!!")])
    password = PasswordField("Password",validators=[DataRequired("Required")])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired() , EqualTo('password', message = "Passwords must Match!!")])
    submit = SubmitField("Submit")

class ArrangeSessionForm(FlaskForm):
    session_name = StringField("Name of Session",validators=[DataRequired("Name Required!!!")])
    session_domain = StringField("Domain of Session",validators=[DataRequired("Domain Required!!!")])
    session_date = DateField("Date to be Conducted",validators=[DataRequired("Date Required"),],format='%Y-%m-%d')
    session_time = StringField("Time to be Conducted",validators=[DataRequired("Date Required"),],render_kw={"placeholder": "HHMMSS"})
    submit = SubmitField("Submit")

     