from flask import Flask, render_template, request, jsonify, send_from_directory , redirect, url_for, flash, get_flashed_messages, make_response
from POC.forms import FeedbackForm, LoginForm, RegistrationForm, ArrangeSessionForm, QuestionForm
from flask_login import current_user, login_user , logout_user, login_required, user_logged_in
from flask_mail import Message, Attachment
from POC import app,db,mail
from POC.models import Admin, Session, StudInfo, Response, Feedback, Question
from werkzeug.urls import url_parse
import datetime,string,json,boto3,os
from datetime import timedelta
from dateutil.relativedelta import *
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from flask_weasyprint import render_pdf
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from .config import base_dir
from threading import Thread

answer = ""
session = ""
comprehend = client = boto3.client('comprehend')

def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


def calcAnswers(responses):
    questions = {'Q1':{'YES':0,'NO':0},'Q2':{'YES':0,'NO':0},'Q3':{'YES':0,'NO':0},'Q4':{'YES':0,'NO':0},'Q5':{'YES':0,'NO':0}}
    switcher ={ 1:'Q1',2:'Q2',3:'Q3',4:'Q4',5:'Q5'}
    for resp in responses:
        t = resp.answer.split(',')
        for i,ans in enumerate(t,start=1):
            questions[switcher[i]][ans] = questions[switcher[i]][ans]+1
    return questions

List_of_factor = ['practical','content','programming','presented','assignments','instructor',
                  'explained','skills','basics','knowledege','topics','professor',
                  'explaining','helped','performance','note','services','clear','qualified',
                  'instruction','theoretical','mentors','assistance','sound','communicator',
                  'staff','presentation','teaching','teacher','practice','engaging','structure','quizzes',
                  'graphs','presenter','explains','specialisation','overview','professors'
                  'application','explain','resources','tools','covered','knowledgeable','lectures','present',
                  'applications','structured','graph','english','presentations',
                  'delivery','technologies','design','technique','organised','organized','contents','speaker',
                  'details','implement','fundamentals','map','theory','advanced',
                  'notes','cases','teaches','skill','team','venue','environment','friendly',
                  'wellstructured','program','discussion','techniques','entertaining','instructors','module',
                  'conceptual','explanations','implementation','approach','presenting','speak',
                  'coding','managed','methods','test','described','speaking','language','screen','video','audio',
                  'audible','implementing','statistical','graphical','visualize','animation','location','clarity',
                  'method','visualization','visualisation','detailed','members','modules','professional',
                  'handson','atmosphere','facilitator','balance','indepth','faculty','accessible',
                  'seminar presenter','activities','management','talented','information','guidance','example',
                  'interactive','discuss','excellent','chart','scope',
                  'languages','programs','concepts','characteristics','videos','technology','informative',
                  'examples','exercise','speakers','teach','teams','materials','structures',
                  'projects','planning','specialization','code','explanation','format','concept','proficiency',
                  'expert','experts','accent','powerpoint','slide'
                 ]

def summarization(id):
    summarizer=LexRankSummarizer()
    """Summarization and Factors influnce for POSITIVE feedbacks"""
    pos_query = Feedback.query.filter_by(sentiment='POSITIVE').filter_by(session=id).all()
    neg_query = Feedback.query.filter_by(sentiment='NEGATIVE').filter_by(session=id).all()
    if len(pos_query) == 0 and len(neg_query) == 0:
        return "0"
    else:     
        pos_text = ""
        for i in range(len(pos_query)):
            pos_text = pos_text + str(pos_query[i].description)

        cleaned_pos_text = pos_text.lower().translate(str.maketrans('', '', string.punctuation))
        tokenized_pos_words = word_tokenize(cleaned_pos_text, "english")
        final_pos_words = []
        for word in tokenized_pos_words:
            if word not in stopwords.words('english'):
                final_pos_words.append(word)

        """Counting Factors for POSITIVE"""
        w = Counter(final_pos_words) 
        a={}
        for x in List_of_factor:
            if x in w.keys():
                a[x]=w[x]
        pos_fact = sorted(a.items(), key=lambda x: x[1],reverse=True)    

        """Summary of POSITIVE"""
        parser=PlaintextParser.from_string(pos_text,Tokenizer("english"))
        summ_Pos = ""
        abstract_pos = summarizer(parser.document,1)
        for sentence in abstract_pos:
            summ_Pos = summ_Pos + str(sentence)

        """Summarization and Factors influnce for NEGATIVE feedbacks"""
        neg_text = ""
        for i1 in range(len(neg_query)):
            neg_text= neg_text + str(neg_query[i1].description)

        cleaned_neg_text = neg_text.lower().translate(str.maketrans('', '', string.punctuation))
        tokenized_neg_words = word_tokenize(cleaned_neg_text, "english")
        final_neg_words = []
        for word in tokenized_neg_words:
            if word not in stopwords.words('english'):
                final_neg_words.append(word)

        """Counting Factors for NEGATIVE"""
        w = Counter(final_neg_words)
        b={}
        for x in List_of_factor:
            if x in w.keys():
                b[x]=w[x]
        neg_fact = sorted(b.items(), key=lambda x: x[1],reverse=True)
        """Summary of NEGATIVE"""
        parser=PlaintextParser.from_string(neg_text,Tokenizer("english"))
        summ_Neg= " "
        abstract_neg = summarizer(parser.document,1)
        for sentence in abstract_neg:
            summ_Neg = summ_Neg + str(sentence)

        return {'cnt_pos': pos_fact[0:5] , 'cnt_neg': neg_fact[0:5],'summ_pos':summ_Pos,'summ_neg':summ_Neg }    
        #return render_template('xyz.html',freq1=dict,summary=summaryP,freq=dict1,abst=summaryN)

@app.route("/certificate",methods=['POST'])
def genPDF():
    name=request.args.get('s_name')
    session_name=request.args.get('session_name')
    domain=request.args.get('domain')
    cert = request.args.get('cert')
    """ Generate PDF Certificate """
    return render_pdf(url_for('cert',s_name = name,session_name=session_name,domain = domain ,date = datetime.date.today(),cert=cert,_external=True),download_filename="certificate.pdf")#,redirect(url_for('success'))

@app.route("/success",methods=['POST'])
def success():
    s_name=request.args.get('s_name')
    session_name=request.args.get('session_name')
    domain=request.args.get('domain')
    cert = request.args.get('cert')
    return render_template("success.html",s_name=s_name,session_name=session_name,domain=domain,cert=cert)

@app.route('/cert',methods=['GET','POST'])
def cert():
    s_name=request.args.get('s_name')
    session_name=request.args.get('session_name')
    domain=request.args.get('domain')
    date=request.args.get('date')
    cert = request.args.get('cert')
    return render_template('certificate.html',s_name=s_name,domain=domain,session_name=session_name,date = date,cert=cert)



@app.route("/",methods = ['GET'])
def start():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("start.html",title = "Home")    


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

@app.route("/arrange",methods=['POST'])
def arrange():
    adata = json.loads(request.args.get('adata'))
    qdata = json.loads(request.args.get('qdata'))
    cert = request.args.get('cert')
    update = int(request.args.get('flag'))
    if update:
        s = Session.query.filter_by(s_id=update).first()
        s.name = adata['session_name']
        s.domain = adata['session_domain']
        s.scheduled_on = adata['session_date'].replace("T"," ")
        s.cert = cert
        q = Question.query.filter_by(s_id=update).all()
        q[0].question = qdata['Q1']
        q[1].question = qdata['Q2']
        q[2].question = qdata['Q3']
        q[3].question = qdata['Q4']
        q[4].question = qdata['Q5']
        db.session.commit()
    else:
        session = Session(name = adata['session_name'] ,domain = adata['session_domain'] ,scheduled_on= adata['session_date'].replace("T"," "), cert=cert)
        db.session.add(session)
        db.session.commit()
        objects = [
        Question(question= qdata['Q1'], s_id= session.s_id),
        Question(question= qdata['Q2'], s_id= session.s_id),
        Question(question= qdata['Q3'], s_id= session.s_id),
        Question(question= qdata['Q4'], s_id= session.s_id),
        Question(question= qdata['Q5'], s_id= session.s_id),
        ]
        db.session.bulk_save_objects(objects)
        db.session.commit()
        flash("Session created Successfully!!")
    return "success"



@app.route("/schedule",methods=['GET'])
@login_required
def schedule():
    """To arrange sessions"""
    arrangeform = ArrangeSessionForm()
    questionform = QuestionForm()
    CERT_SYSTEM = base_dir+url_for('static',filename='img/certificate')
    itemList = os.listdir(CERT_SYSTEM)
    return render_template("createsession.html", title = "Schedule Session", arrangeform = arrangeform, qform=questionform, itemList=itemList,CERT_SYSTEM = CERT_SYSTEM)

@app.route("/feedback",methods = ['GET'])
def start_session():
    l=[]
    t = db.session.query(Session).filter(Session.scheduled_on < datetime.datetime.now()).all()
    for obj in t:
        dateTimeA = datetime.datetime.now()
        dateTimeB = obj.scheduled_on
        dateTimeDifference = dateTimeA - dateTimeB
        dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 3600
        # print("dateTimeDifferenceInHours",dateTimeDifferenceInHours,obj.name)
        if dateTimeDifferenceInHours > 0:
            l.append(dateTimeDifferenceInHours)
    a = min(l)
    q = Question.query.filter_by(s_id=t[l.index(a)].s_id).all()
    return render_template("welcome.html",session = t[l.index(a)].domain,question=q)

@app.route("/feedback_form",methods=['GET'])
def feedback_form():
    form = FeedbackForm()
    global answer
    answer = request.args.get('data')
    s_domain = request.args.get('session')
    """Get session_id """
    global session 
    session = Session.query.filter_by(domain=s_domain).first()
    return render_template("feedbackform.html",form=form)

@app.route("/feedback",methods=['POST'])
def getFeedback():
    print("in /feedback POST")
    form = FeedbackForm(request.form)
    now = datetime.datetime.now().time()
    if form.validate_on_submit():
        stud = StudInfo(mobile = form.contact.data,name = form.name.data,email = form.email.data,address = form.address.data,city = form.city.data)
        """Add response"""
        res = Response(answer = answer,session = session.s_id,stud_mobile = form.contact.data)
        """Add Association"""
        stud.session.append(session)
        db.session.add(stud)
        db.session.add(res)
        """Add Feedback
            API call for sentiment  
        """
        sentiment = comprehend.detect_sentiment(Text=form.feedback.data, LanguageCode='en')
        feedback = Feedback(date = datetime.date.today(),time = now ,areaofinterest = form.areaofinterest.data,description = form.feedback.data,session = session.s_id,mobile = stud.mobile, sentiment = sentiment['Sentiment'] )
        db.session.add(feedback)
        db.session.commit()
        cert = Session.query.filter_by(s_id=session.s_id).first().cert
        return redirect(url_for('success',s_name = form.name.data,session_name = session.name ,domain = session.domain ,cert = cert),code = 307)#render_pdf(url_for('cert',s_name = form.name.data,session_name=session.name,domain = session.domain ,date = datetime.date.today(),cert=cert,_external=True),download_filename="certificate.pdf")
    return render_template("feedbackform.html",form=form)    


@app.route("/show",methods=['GET','POST'])
def getStudents():
    """To view all the Student attendees"""
    query = db.session.query(Feedback.mobile, Feedback.description, Session.name).filter(Feedback.session == Session.s_id).subquery()
    students = db.session.query(StudInfo.name , StudInfo.email , StudInfo.city, query.c.description, query.c.name).filter(StudInfo.mobile == query.c.mobile).order_by(StudInfo.name).all()
    return render_template("students.html",students = students,title="Attendees")#,next=next_url,prev=prev_url,pages=pages,cur_page=cur_page)


@app.route("/getCity",methods=['GET'])
def getCity():
    city = request.args.get('city',"Pune",type = str)
    query = db.session.query(Feedback.mobile, Feedback.description, Session.name).filter(Feedback.session == Session.s_id).subquery()
    students = db.session.query(StudInfo.name , StudInfo.email , StudInfo.city, query.c.description, query.c.name).filter(StudInfo.mobile == query.c.mobile).filter(StudInfo.city == city).order_by(StudInfo.name).all()
    return { 'students':students }
    

@app.route("/getSession",methods=['GET'])
def getSession():
    session = request.args.get('session',"",type = str)
    query = db.session.query(Feedback.mobile, Feedback.description, Session.name).filter(Feedback.session == Session.s_id).filter(Session.name == session).subquery()
    students = db.session.query(StudInfo.name , StudInfo.email , StudInfo.city, query.c.description, query.c.name).filter(StudInfo.mobile == query.c.mobile).order_by(StudInfo.name).all()
    return { 'students':students }

@app.route("/getSession_invite",methods=['GET'])
def getSession_invite():
    date = datetime.datetime.now()
    date = date + relativedelta(months=-6)
    session = request.args.get('session',"",type = str)
    query = db.session.query(Feedback.mobile, Feedback.areaofinterest, Session.name).filter(Feedback.session == Session.s_id).filter(Session.name == session).filter(Session.scheduled_on > date).subquery()
    students = db.session.query( StudInfo.email ,StudInfo.name,  query.c.areaofinterest, query.c.name).filter(StudInfo.mobile == query.c.mobile).order_by(StudInfo.name).all()
    return { 'students':students }

@app.route("/getAOI_invite",methods=['GET'])
def getAOI_invite():
    date = datetime.datetime.now()
    date = date + relativedelta(months=-6)
    areaOI = request.args.get('areaOI')
    query = db.session.query(Feedback.mobile, Feedback.areaofinterest, Session.name).filter(Feedback.session == Session.s_id).filter(Session.scheduled_on > date).subquery()
    students = db.session.query(StudInfo.email , StudInfo.name , query.c.areaofinterest, query.c.name).filter(StudInfo.mobile == query.c.mobile).filter(query.c.areaofinterest== areaOI).order_by(StudInfo.name).all()
    return { 'students':students }
    


@app.route('/report/<s_id>',methods=['GET','POST'])
def genReport(s_id):
    response = Response.query.filter_by(session=s_id).first()
    if not response:
        id = 0
    else:
        id=response.session    
    session = Session.query.filter_by(s_id=s_id).first()
    name=session.name
    return render_template("chart.html",id=id,name=name,title="Report")
    

@app.route('/getReport',methods=['GET','POST'])
def REPORT():
    id = request.args.get('id')
    response = Response.query.filter_by(session=id).all()
    if not response:
        return "0"
    questions = calcAnswers(response)
    feed_pos = db.session.query(db.func.count(Feedback.sentiment)).filter_by(sentiment='POSITIVE').filter_by(session=id).group_by(Feedback.sentiment).first()
    feed_neg = db.session.query(db.func.count(Feedback.sentiment)).filter_by(sentiment='NEGATIVE').filter_by(session=id).group_by(Feedback.sentiment).first()
    questions['feed_pos']= int(feed_pos[0])
    questions['feed_neg']=int(feed_neg[0])
    return questions

@app.route("/getSummary",methods = ['GET','POST'])
def getSummary():
    return summarization(request.args.get('id'))

@app.route("/sessions",methods=['GET','POST'])
def getSessions():
    """To view arranged sessions"""
    sessions = Session.query.paginate(1,app.config['ENTRIES_PER_PAGE'],False)
    return render_template("sessions.html",title='Sessions',sessions = sessions.items)

@app.route("/delsession",methods=['GET','POST'])
def del_Session():
    """To delete arranged sessions"""
    # q = Question.query.filter_by(s_id = request.args.get('s_id')).all()
    # db.session.delete(q) 
    s = Session.query.filter_by(s_id = request.args.get('s_id')).first()
    db.session.delete(s)
    db.session.commit()
    flash("Session Deleted!!")
    l = get_flashed_messages()
    return l[0]

@app.route("/editsession/<id>",methods=['GET','POST'])
def edit_Session(id):
    print(id)
    CERT_SYSTEM = base_dir+url_for('static',filename='img/certificate')
    itemList = os.listdir(CERT_SYSTEM)
    s = Session.query.filter_by(s_id = id).first()
    q = Question.query.filter_by(s_id = id).all()
    form = ArrangeSessionForm()
    qform = QuestionForm()       
    return render_template("createsession.html", title = "Schedule", form = form,sessions=s,questions=q,qform=qform,itemList=itemList,CERT_SYSTEM = CERT_SYSTEM)

@app.route("/getdata",methods=['GET'])
def getAOI():
    data_aoi = db.session.query(db.func.count(Feedback.areaofinterest),Feedback.areaofinterest).group_by(Feedback.areaofinterest).all()
    data_sentiment = db.session.query(Feedback.sentiment ,db.func.count(Feedback.sentiment)).group_by(Feedback.sentiment).all()
    d = {'AOI': data_aoi , 'sentiment':data_sentiment} 
    return d

@app.route("/users",methods=['GET','POST'])
def getUsers():
    """To view users"""
    users= Admin.query.paginate(1,app.config['ENTRIES_PER_PAGE'],False)
    return render_template("users.html",title='Users',users = users.items)

@app.route("/deluser",methods=['GET','POST'])
def del_User():
    """To delete User"""
    u = Admin.query.filter_by(mobile = request.args.get('mobile')).first()
    db.session.delete(u)
    db.session.commit()
    flash("User Deleted!!")
    l = get_flashed_messages()
    return l[0]


@app.route("/filter",methods=['GET'])
def filter():	
    city = db.session.query(StudInfo.city).distinct().all()
    ses = db.session.query(Session.name).filter(Session.scheduled_on < datetime.datetime.now()).distinct().all()
    return {'city': city,'session':ses}   
    
@app.route("/filter_invite",methods=['GET'])
def filter_invites():
    areaOI=db.session.query(Feedback.areaofinterest).distinct().all()	
    ses = db.session.query(Session.name).distinct().all()
    return {'areaOI':areaOI,'session':ses} 

@app.route("/sendEmail_invites",methods=['GET','POST'])
def sendEmail_invites():
        """Mail the invites"""
        mail = request.args.get('mail').split(',')
        sid = request.args.get('session_id')
        query_name= db.session.query(Session.name).filter(Session.s_id == sid).first()
        query_schedule= db.session.query(Session.scheduled_on).filter(Session.s_id == sid).scalar()
        date = query_schedule.strftime("%d %B %Y")
        time = query_schedule.strftime("%H:%M")
        msg = Message(subject = 'Invitation for new Session',recipients = mail , body = 'Dear Participants \n Prudent Software and Grooming Acadamy invite you to attend the  '+str(query_name[0])+'seminar which will be held on '+date+' at '+time+'.\n We would be glad if you participate in this seminar as it will help to shape your career and resolve doubts regarding the same.\n\n\n Regards \n Prudent \n 09309799864 ',sender = 'developernil98@gmail.com')
        thr = Thread(target=send_async_email, args=[msg])
        thr.start()
        return "Invite has been sent!"


@app.route("/invites",methods=['GET','POST'])
def Invites():
    # apply filter of date(6 months)
    date = datetime.datetime.now()
    s = Session.query.filter(Session.scheduled_on > datetime.datetime.now()).all()
    date = date + relativedelta(months=-6)
    query = db.session.query(Feedback.mobile, Feedback.areaofinterest, Session.name).filter(Feedback.session == Session.s_id).filter(Session.scheduled_on > date).subquery()
    students = db.session.query(StudInfo.email,StudInfo.name , query.c.areaofinterest,query.c.name).filter(StudInfo.mobile== query.c.mobile).order_by(StudInfo.name).all()
    
    return render_template("Invitess.html",students=students,title="Invites",sessions=s)#,next=next_url,prev=prev_url,pages=pages,cur_page=cur_page)
   

@app.route("/service-worker.js",methods = ['GET','POST'])
def load_service():
    return send_from_directory(app.config['SERVICE_WORKER_PATH'],'service-worker.js')


@app.errorhandler(404)
def page_not_found(error):
    return 'This route does not exist {}'.format(request.url), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return 'This method is not allowed {}'.format(request.method), 405

@app.errorhandler(500)
def internal_server_error(error):
    return 'This application has internal error please contact admin. {}'.format(request.url), 405