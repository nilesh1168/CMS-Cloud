from POC import db,login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(ident):
  return Admin.query.get(int(ident))

class Admin(db.Model,UserMixin):
    __tablename__='Admin_Table'
    username = db.Column(db.String(35),unique = True)
    email = db.Column(db.String(50), nullable = False)
    mobile = db.Column(db.BigInteger(),primary_key = True, autoincrement=False)
    password_hash = db.Column(db.String(150))
    
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return  check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.mobile
        
    def __repr__(self):
        return 'User : {}'.format(self.username)  

class Question(db.Model):
    __tablename__='Question_Table'
    q_id = db.Column(db.Integer(),primary_key=True)
    question = db.Column(db.String(100))

    def __repr__(self):
        return 'Question : {}'.format(self.question) 

Session_Stud = db.Table('Session_Stud',
    db.Column('session_id',db.Integer(),db.ForeignKey('Session.s_id')),
    db.Column('stud_id',db.BigInteger(),db.ForeignKey('Student_Info.mobile'))
)

class Session(db.Model):
    __tablename__='Session'
    s_id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(30))
    domain = db.Column(db.String(20))
    scheduled_on = db.Column(db.DateTime(),nullable=False)

    def __repr__(self):
        return 'Domain : {}'.format(self.domain)

class Feedback(db.Model):
    __tablename__='Feedback'
    f_id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date())
    time = db.Column(db.Time())
    areaofinterest = db.Column(db.String(20),nullable = False)
    description = db.Column(db.String(200),nullable = False)
    session = db.Column(db.Integer(),db.ForeignKey('Session.s_id'))
    mobile = db.Column(db.BigInteger(),db.ForeignKey('Student_Info.mobile'))
    sentiment = db.Column(db.String(10),nullable = False)

    def __repr__(self):
        return 'Description : {}'.format(self.description)

class Response(db.Model):
    __tablename__='Response'
    response_id = db.Column(db.Integer(),primary_key = True)
    answer = db.Column(db.String(50))
    session = db.Column(db.Integer(),db.ForeignKey('Session.s_id'))
    stud_mobile = db.Column(db.BigInteger(),db.ForeignKey('Student_Info.mobile'))
    def __repr__(self):
        return 'Answers : {}'.format(self.answer)




class StudInfo(db.Model):
    __tablename__ = 'Student_Info'
    mobile = db.Column(db.BigInteger(), primary_key = True,autoincrement=False)
    name = db.Column(db.String(70))
    email = db.Column(db.String(50))
    address = db.Column(db.String(150))
    city = db.Column(db.String(30))
    feedback = db.relationship('Feedback',backref='Student_Info')
    response = db.relationship('Response',backref='Student_Info')
    session = db.relationship('Session',secondary='Session_Stud',backref='Student_Info')
    
    def __repr__(self):
        return 'Mobile : {}'.format(self.mobile)    





