from flask import Flask, render_template, request, jsonify, send_from_directory , redirect, url_for, flash, get_flashed_messages
from POC.forms import FeedbackForm, LoginForm, RegistrationForm, ArrangeSessionForm
from flask_login import current_user, login_user , logout_user, login_required, user_logged_in
from POC import app,db
from POC.models import Admin, Session, StudInfo, Response, Feedback
from werkzeug.urls import url_parse
import datetime
from POC.entity import feedbackEntity
import boto3

comprehend = client = boto3.client('comprehend')

@app.route("/",methods = ['GET','POST'])
@login_required
def home():
    sessions = db.session.query(Session).filter(Session.scheduled_on > datetime.datetime.now()).all()
    return render_template("dashboard.html",title='Dashboard',sessions = sessions)    

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        admin = Admin(username = form.username.data, email = form.email.data, mobile = form.mobile.data )
        admin.set_password(form.password.data)
        # msg = Message(subject = 'Welcome to Task Lister',recipients = [form.email.data], body = 'Welcome to Daily Task Lister '+form.username.data+'.\n This mail is to inform that you are successfully registered on Task Lister.\n Thank You!!!!',sender = 'developernil98@gmail.com')
        # mail.send(msg)
        # message = client.messages.create(to="+91"+form.mobile.data ,from_="+12509002936",body="Thank You for registering with Daily Task Lister!")
        db.session.add(admin)
        
        db.session.commit()
        flash("Registered Successfully!!")
        return redirect(url_for('login'))        
    return render_template('registration.html',title="Register", form = form)


@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or Password")
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html',title = 'Login', form = form)    


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/schedule",methods=['GET','POST'])
@login_required
def schedule():
    """To arrange sessions"""
    form = ArrangeSessionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.session_domain.data)
            print(type(form.session_date.data))
            session = Session(name = form.session_name.data ,domain = form.session_domain.data ,scheduled_on= form.session_date.data)
            db.session.add(session)
            db.session.commit()
            flash("Session created Successfully!!")
            return redirect(url_for('schedule'))
    return render_template("createsession.html", title = "Schedule", form = form)

@app.route("/feedback",methods = ['GET'])
def start_session():
    l=[]
    t = db.session.query(Session).filter(Session.scheduled_on < datetime.datetime.now()).all()
    for obj in t:
        dateTimeA = datetime.datetime.now()
        dateTimeB = obj.scheduled_on
        dateTimeDifference = dateTimeA - dateTimeB
        dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 3600
        print("dateTimeDifferenceInHours",dateTimeDifferenceInHours,obj.name)
        if dateTimeDifferenceInHours > 0:
            l.append(dateTimeDifferenceInHours)
    a = min(l)
    print("inside /feedback",t[l.index(a)].domain)
    return render_template("welcome.html",session = t[l.index(a)].domain)

@app.route("/feedback_form",methods=['GET'])
def feedback_form():
    form = FeedbackForm()
    answer = request.args.get('data')
    s_domain = request.args.get('session')
    print(answer)
    print(s_domain)
    """Get session_id """
    session = Session.query.filter_by(domain=s_domain).first()
    print(type(session))
    print(session.s_id)
    feedbackEntity.answer = answer
    feedbackEntity.session = session
    return render_template("feedbackform.html",form=form)

@app.route("/getFeedback",methods=['GET','POST'])
def getFeedback():
    form = FeedbackForm(request.form)
    now = datetime.datetime.now().time()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        stud = StudInfo(mobile = form.contact.data,name = form.name.data,email = form.email.data,address = form.address.data,city = form.city.data)
        """Add response"""
        res = Response(answer = feedbackEntity.answer,session = feedbackEntity.session.s_id,stud_mobile = form.contact.data)
        """Add Association"""
        stud.session.append(feedbackEntity.session)
        db.session.add(stud)
        db.session.add(res)
        db.session.commit()
        """Add Feedback
            API call for sentiment  
        """
        sentiment = comprehend.detect_sentiment(Text=form.feedback.data, LanguageCode='en')
        feedback = Feedback(date = datetime.date.today(),time = now ,areaofinterest = form.areaofinterest.data,description = form.feedback.data,session = feedbackEntity.session.s_id,mobile = stud.mobile, sentiment = sentiment['Sentiment'] )
        db.session.add(feedback)
        db.session.commit()
        return render_template('test.html')
    return render_template("feedbackform.html",form=form)    

@app.route("/show",methods=['GET','POST'])
def getStudents():
    """To view all the Student attendees"""
    page = request.args.get('page', 1,type = int)

    query = db.session.query(Feedback.mobile, Feedback.description, Session.name).filter(Feedback.session == Session.s_id).subquery()
    students = db.session.query(StudInfo.name , StudInfo.email , StudInfo.city, query.c.description, query.c.name).filter(StudInfo.mobile == query.c.mobile).paginate(page,app.config['ENTRIES_PER_PAGE'],False)
    pages = students.pages
    cur_page = students.page
    next_url = url_for('getStudents', page=students.next_num) if students.has_next else None
    prev_url = url_for('getStudents', page=students.prev_num) if students.has_prev else None
    return render_template("students.html",students = students,next=next_url,prev=prev_url,pages=pages,cur_page=cur_page)



@app.route("/sessions",methods=['GET','POST'])
def getSessions():
    """To view arranged sessions"""
    sessions = Session.query.paginate(1,app.config['ENTRIES_PER_PAGE'],False)
    return render_template("sessions.html",title='Sessions',sessions = sessions.items)

@app.route("/delsession/<s_id>",methods=['GET','POST'])
def del_Session(s_id):
    """To delete arranged sessions"""
    s = Session.query.filter_by(s_id = s_id).first()
    db.session.delete(s)
    db.session.commit()
    flash("Session Deleted!!")
    l = get_flashed_messages()
    return l[0]
    
@app.route("/getdata",methods=['GET'])
def getAOI():
    data_aoi = db.session.query(Feedback.areaofinterest ,db.func.count(Feedback.areaofinterest)).group_by(Feedback.areaofinterest).all()
    data_sentiment = db.session.query(Feedback.sentiment ,db.func.count(Feedback.sentiment)).group_by(Feedback.sentiment).all()
    d = {'AOI': data_aoi , 'sentiment':data_sentiment} 
    return d

@app.route("/showanswers",methods=['GET','POST'])
def showAnswers():
    arr = request.args.get("data")
    print(type(arr))
    #print(request.environ['REMOTE_ADDR'])
    print(request.environ['HTTP_X_FORWARDED_FOR'])
    #print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    return render_template('answers.html',answer=arr)


@app.route("/service-worker.js",methods = ['GET','POST'])
def load_service():
    return send_from_directory(app.config['SERVICE_WORKER_PATH'],'service-worker.js')

@app.errorhandler(404)
def page_not_found(error):
    return 'This route does not exist {}'.format(request.url), 404
