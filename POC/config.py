import os

base_dir = os.path.abspath(os.path.dirname(__file__))
class Config():
    """
    This is our configuration class
    database url and other things here...
"""
    ENTRIES_PER_PAGE = 10 #this is the number of records that will be displayed on single page : eg 10 students on one page
    SECRET_KEY = "Asecretkey" # this is the applications secret key
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin123@prudent.cgpamkh0cvsh.us-west-2.rds.amazonaws.com:3306/dummy' # DB URL //username:password@address:port/dbname this is the format. 
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SERVICE_WORKER_PATH = "/media/nilesh/Work/BE Project(Sponsored)/POC Feedback Form/POC" #this is the service worker by which we get notifications.


