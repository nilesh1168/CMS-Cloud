from flask import Flask, render_template, request, jsonify, send_from_directory , redirect, url_for, flash, get_flashed_messages, make_response
from POC.forms import FeedbackForm, LoginForm, RegistrationForm, ArrangeSessionForm
from flask_login import current_user, login_user , logout_user, login_required, user_logged_in
from flask_mail import Message, Attachment
from POC import app,db,mail
from POC.models import Admin, Session, StudInfo, Response, Feedback
from werkzeug.urls import url_parse
import datetime
from POC.entity import feedbackEntity
import boto3
from wkhtmltopdfwrapper import WKHtmlToPdf

comprehend = client = boto3.client('comprehend')

def calcAnswers(responses):
    questions = {'Q1':{'YES':0,'NO':0},'Q2':{'YES':0,'NO':0},'Q3':{'YES':0,'NO':0},'Q4':{'YES':0,'NO':0},'Q5':{'YES':0,'NO':0}}
    switcher ={ 1:'Q1',2:'Q2',3:'Q3',4:'Q4',5:'Q5'}
    for resp in responses:
        t = resp.answer.split(',')
        for i,ans in enumerate(t,start=1):
            questions[switcher[i]][ans] = questions[switcher[i]][ans]+1
    return questions




@app.route('/cert')
def cert(s_name,session_name,domain,date):
    return render_template('certificate.html',s_name=s_name,domain=domain,session_name=session_name,date = date)


@app.route("/",methods = ['GET'])
def start():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("start.html")    


@app.route("/dashboard",methods = ['GET','POST'])
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
            session = Session(name = form.session_name.data ,domain = form.session_domain.data ,scheduled_on= form.session_date.data)
            db.session.add(session)
            db.session.commit()
            flash("Session created Successfully!!")
            return redirect(url_for('getSessions'))
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
        #db.session.commit()
        """Add Feedback
            API call for sentiment  
        """
        sentiment = comprehend.detect_sentiment(Text=form.feedback.data, LanguageCode='en')
        feedback = Feedback(date = datetime.date.today(),time = now ,areaofinterest = form.areaofinterest.data,description = form.feedback.data,session = feedbackEntity.session.s_id,mobile = stud.mobile, sentiment = sentiment['Sentiment'] )
        db.session.add(feedback)
        #db.session.commit()
        """ Generate PDF Certificate """ 
        wkhtmltopdf = WKHtmlToPdf('-T 10 -B 10 -O Landscape -s Letter --zoom 1.5')
        wkhtmltopdf.render(url_for('cert',s_name = form.name.data,session_name=feedbackEntity.session.name,domain = feedbackEntity.session.domain ,date =datetime.date.today() ,_external=True), app.config['CERT_PATH']+"cert.pdf")
        """Mail the certificate to the participant"""
        msg = Message(subject = 'Prudent Participation Certificate',recipients = [form.email.data], body = 'This is an appreciation certificate from Prudent Grooming and Software Academy.\n We Thank You for participating in the session '+feedbackEntity.session.name+'.\n We hope to see you again in upcoming sessions!!!\n Thanks and Regards \n Prudent Grooming and Software Academy \n (PSGA)',sender = 'developernil98@gmail.com')
        with app.open_resource("certificate/cert.pdf") as fp:
            msg.attach("certificate.pdf",content_type="application/pdf", data=fp.read())
        mail.send(msg)

        return render_template('success.html')
    return render_template("feedbackform.html",form=form)    


@app.route("/show",methods=['GET','POST'])
def getStudents():
    """To view all the Student attendees"""
    return render_template("students.html")#,students = students,next=next_url,prev=prev_url,pages=pages,cur_page=cur_page)

@app.route("/show_all_students",methods=['GET'])
def getAllStudents():
    """To view all the Student attendees"""
    page = request.args.get('page', 1,type = int)
    query = db.session.query(Feedback.mobile, Feedback.description, Session.name).filter(Feedback.session == Session.s_id).subquery()
    students = db.session.query(StudInfo.name , StudInfo.email , StudInfo.city, query.c.description, query.c.name).filter(StudInfo.mobile == query.c.mobile).order_by(StudInfo.name).paginate(page,app.config['ENTRIES_PER_PAGE'],False)
    pages = students.pages
    cur_page = students.page
    next_url = url_for('getStudents', page=students.next_num) if students.has_next else None
    prev_url = url_for('getStudents', page=students.prev_num) if students.has_prev else None
    return { 'students':students.items , 'pages': pages, 'cur_page':cur_page ,"next_url": next_url ,"prev_url": prev_url}    

@app.route("/getCity",methods=['GET'])
def getCity():
    city = request.args.get('city',"Pune",type = str)
    page = request.args.get('page', 1,type = int)
    query = db.session.query(Feedback.mobile, Feedback.description, Session.name).filter(Feedback.session == Session.s_id).subquery()
    students = db.session.query(StudInfo.name , StudInfo.email , StudInfo.city, query.c.description, query.c.name).filter(StudInfo.mobile == query.c.mobile).filter(StudInfo.city == city).order_by(StudInfo.name).paginate(page,app.config['ENTRIES_PER_PAGE'],False)
    pages = students.pages
    cur_page = students.page
    next_url = url_for('getStudents', page=students.next_num) if students.has_next else None
    prev_url = url_for('getStudents', page=students.prev_num) if students.has_prev else None
    return { 'students':students.items , 'pages': pages, 'cur_page':cur_page ,"next_url": next_url ,"prev_url": prev_url}
    

@app.route("/getSession",methods=['GET'])
def getSession():
    session = request.args.get('session',"",type = str)
    page = request.args.get('page', 1,type = int)
    query = db.session.query(Feedback.mobile, Feedback.description, Session.name).filter(Feedback.session == Session.s_id).filter(Session.name == session).subquery()
    students = db.session.query(StudInfo.name , StudInfo.email , StudInfo.city, query.c.description, query.c.name).filter(StudInfo.mobile == query.c.mobile).order_by(StudInfo.name).paginate(page,app.config['ENTRIES_PER_PAGE'],False)
    pages = students.pages
    cur_page = students.page
    next_url = url_for('getStudents', page=students.next_num) if students.has_next else None
    prev_url = url_for('getStudents', page=students.prev_num) if students.has_prev else None
    return { 'students':students.items , 'pages': pages, 'cur_page':cur_page ,"next_url": next_url ,"prev_url": prev_url}


@app.route('/report/<s_id>',methods=['GET','POST'])
def genReport(s_id):
    response = Response.query.filter_by(session=s_id).first()
    session = Session.query.filter_by(s_id=s_id).first()
    print(type(response))
    return render_template("chart.html",id=response.session,name=session.name,title="Prudent")
    

@app.route('/getReport',methods=['GET','POST'])
def REPORT():
    id = request.args.get('id')
    response = Response.query.filter_by(session=id).all()
    questions = calcAnswers(response)
    return questions


@app.route("/sessions",methods=['GET','POST'])
def getSessions():
    """To view arranged sessions"""
    sessions = Session.query.paginate(1,app.config['ENTRIES_PER_PAGE'],False)
    return render_template("sessions.html",title='Sessions',sessions = sessions.items)

@app.route("/delsession",methods=['GET','POST'])
def del_Session():
    """To delete arranged sessions"""
    s = Session.query.filter_by(s_id = request.args.get('s_id')).first()
    db.session.delete(s)
    db.session.commit()
    flash("Session Deleted!!")
    l = get_flashed_messages()
    return l[0]

@app.route("/editsession/<id>",methods=['GET','POST'])
def edit_Session(id):
    print(id)
    s = Session.query.filter_by(s_id =id).first()
    form = ArrangeSessionForm()
    if request.method == 'POST' and form.validate():
        s.name = form.session_name.data
        s.domain = form.session_domain.data
        s.scheduled_on = form.session_date.data       
        db.session.add(s)
        db.session.commit()
        flash("Session modified Successfully!!")
        return redirect(url_for('getSessions'))        
    return render_template("createsession.html", title = "Schedule", form = form,sessions=s)

@app.route("/getdata",methods=['GET'])
def getAOI1():
    data_aoi = db.session.query(Feedback.areaofinterest ,db.func.count(Feedback.areaofinterest)).group_by(Feedback.areaofinterest).all()
    data_sentiment = db.session.query(Feedback.sentiment ,db.func.count(Feedback.sentiment)).group_by(Feedback.sentiment).all()
    d = {'AOI': data_aoi , 'sentiment':data_sentiment} 
    return d



@app.route("/filter",methods=['GET'])
def filter():
    city = db.session.query(StudInfo.city).distinct().all()
    ses = db.session.query(Session.name).distinct().all()
    return {'city': city,'session':ses }    

@app.route("/send_invites",methods=['GET','POST'])
def sendInvites():
    sessions = db.session.query(Session).filter(Session.scheduled_on > datetime.datetime.now()).all()
    if request.method == 'POST':
        pass
    return render_template("sendinvites.html",sessions=sessions)

@app.route("/service-worker.js",methods = ['GET','POST'])
def load_service():
    return send_from_directory(app.config['SERVICE_WORKER_PATH'],'service-worker.js')

@app.errorhandler(404)
def page_not_found(error):
    return 'This route does not exist {}'.format(request.url), 404

