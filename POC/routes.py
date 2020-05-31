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
from POC.entity import feedbackEntity
from wkhtmltopdfwrapper import WKHtmlToPdf
from threading import Thread
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from .config import base_dir

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
    count =0
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
    neg_query = Feedback.query.filter_by(sentiment='NEGATIVE').filter_by(session=id).all()
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
    count = 0
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




@app.route('/cert',methods=['GET','POST'])
def cert():
    s_name=request.args.get('s_name')
    session_name=request.args.get('session_name')
    domain=request.args.get('domain')
    date=request.args.get('date')
    cert = request.args.get('cert')
    print(cert)
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
    return str(session.s_id)
    # return '5'


@app.route("/schedule",methods=['GET'])
@login_required
def schedule():
    """To arrange sessions"""
    arrangeform = ArrangeSessionForm()
    questionform = QuestionForm()
    CERT_SYSTEM = base_dir+url_for('static',filename='img/certificate')
    itemList = os.listdir(CERT_SYSTEM)
    # if request.method == 'POST':
    #     print("asjv")
    #     if arrangeform.validate_on_submit() and arrangeform.arrange.data:
    #         print("idk")
    #         session = Session(name = arrangeform.session_name.data ,domain = arrangeform.session_domain.data ,scheduled_on= arrangeformform.session_date.data)
    #         db.session.add(session)    
    #         db.session.commit()
    #         flash("Session created Successfully!!")
    #         return redirect(url_for('getSessions'))
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
        print("dateTimeDifferenceInHours",dateTimeDifferenceInHours,obj.name)
        if dateTimeDifferenceInHours > 0:
            l.append(dateTimeDifferenceInHours)
    a = min(l)
    print("inside /feedback",t[l.index(a)].domain)
    q = Question.query.filter_by(s_id=t[l.index(a)].s_id).all()
    print(len(q))
    print(q)
    return render_template("welcome.html",session = t[l.index(a)].domain,question=q)

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
        """ Generate PDF Certificate """
        cert = Session.query.filter_by(s_id=feedbackEntity.session.s_id).first().cert 
        wkhtmltopdf = WKHtmlToPdf('-T 10 -B 10 -O Landscape -s Letter --zoom 1.5')
        wkhtmltopdf.render(url_for('cert',s_name = form.name.data,session_name=feedbackEntity.session.name,domain = feedbackEntity.session.domain ,date =datetime.date.today(),cert=cert,_external=True), app.config['CERT_PATH']+"cert.pdf")
        """Mail the certificate to the participant"""
        msg = Message(subject = 'Prudent Participation Certificate',recipients = [form.email.data], body = 'This is an appreciation certificate from Prudent Grooming and Software Academy.\n We Thank You for participating in the session '+feedbackEntity.session.name+'.\n We hope to see you again in upcoming sessions!!!\n Thanks and Regards \n Prudent Grooming and Software Academy \n (PSGA)',sender = 'developernil98@gmail.com')
        with app.open_resource("certificate/cert.pdf") as fp:
            msg.attach("certificate.pdf",content_type="application/pdf", data=fp.read())
        thr = Thread(target=send_async_email, args=[msg])
        thr.start()
        return render_template('success.html')
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
    print(areaOI)
    query = db.session.query(Feedback.mobile, Feedback.areaofinterest, Session.name).filter(Feedback.session == Session.s_id).filter(Session.scheduled_on > date).subquery()
    students = db.session.query(StudInfo.email , StudInfo.name , query.c.areaofinterest, query.c.name).filter(StudInfo.mobile == query.c.mobile).filter(query.c.areaofinterest== areaOI).order_by(StudInfo.name).all()
    return { 'students':students }
    


@app.route('/report/<s_id>',methods=['GET','POST'])
def genReport(s_id):
    response = Response.query.filter_by(session=s_id).first()
    session = Session.query.filter_by(s_id=s_id).first()
    return render_template("chart.html",id=response.session,name=session.name,title="Report")
    

@app.route('/getReport',methods=['GET','POST'])
def REPORT():
    id = request.args.get('id')
    response = Response.query.filter_by(session=id).all()
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
def getAOI():
    data_aoi = db.session.query(db.func.count(Feedback.areaofinterest),Feedback.areaofinterest).group_by(Feedback.areaofinterest).all()
    data_sentiment = db.session.query(Feedback.sentiment ,db.func.count(Feedback.sentiment)).group_by(Feedback.sentiment).all()
    d = {'AOI': data_aoi , 'sentiment':data_sentiment} 
    print(d)
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
    print(u)
    db.session.delete(u)
    db.session.commit()
    flash("User Deleted!!")
    l = get_flashed_messages()
    return l[0]


@app.route("/filter",methods=['GET'])
def filter():	
    city = db.session.query(StudInfo.city).distinct().all()
    ses = db.session.query(Session.name).distinct().all()
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
        
        #print('Dear Participants \n Prudent Software and Grooming Acadamy invite you to attend the  '+str(query_name[0])+'seminar which will be held on '+date+' at '+time+'.\n We would be glad if you participate in this seminar as it will help to shape your career and resolve doubts regarding the same.\n\n\n Regards \n Prudent \n 09309799864 ')
        
        
        # msg = Message(subject = 'Invitation for new Session',recipients = mail , body = 'Dear Participants \n Prudent Software and Grooming Acadamy invite you to attend the  '+str(query_name[0])+'seminar which will be held on '+date+' at '+time+'.\n We would be glad if you participate in this seminar as it will help to shape your career and resolve doubts regarding the same.\n\n\n Regards \n Prudent \n 09309799864 ',sender = 'developernil98@gmail.com')
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
