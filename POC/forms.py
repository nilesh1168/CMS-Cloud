from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length, EqualTo, Email, Length
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, PasswordField, DateTimeField
from wtforms.fields.html5 import DateTimeLocalField

class FeedbackForm(FlaskForm):
    name = StringField("Name")
    contact = StringField("Mobile", validators= [DataRequired("Contact Required!!!!"), Length(min = 10,max = 10,message = "Mobile Number should be 10 digits!")])
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
    mobile = StringField("Mobile",validators=[DataRequired("Contact Required!!"),Length(min = 10,max = 10,message = "Mobile Number should be 10 digits!")])
    password = PasswordField("Password",validators=[DataRequired("Required")])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired() , EqualTo('password', message = "Passwords must Match!!")])
    submit = SubmitField("Submit")

class ArrangeSessionForm(FlaskForm):
    session_name = StringField("Name of Session",validators=[DataRequired("Name Required!!!")])
    session_domain = StringField("Domain of Session",validators=[DataRequired("Domain Required!!!")])
    session_date = DateTimeLocalField("Date and Time to be Conducted",format='%Y-%m-%dT%H:%M',validators=[DataRequired("Date Required"),])
    #session_time = StringField("Time to be Conducted",validators=[DataRequired("Date Required"),],render_kw={"placeholder": "HHMMSS"})


class QuestionForm(FlaskForm):
    Q1 = StringField("Question 1",validators=[DataRequired("Question Required!!!")])
    Q2 = StringField("Question 2",validators=[DataRequired("Question Required!!!")])     
    Q3 = StringField("Question 3",validators=[DataRequired("Question Required!!!")])     
    Q4 = StringField("Question 4",validators=[DataRequired("Question Required!!!")])     
    Q5 = StringField("Question 5",validators=[DataRequired("Question Required!!!")])     
     
