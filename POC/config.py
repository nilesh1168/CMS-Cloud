import os

base_dir = os.path.abspath(os.path.dirname(__file__))
class Config():
    """
    This is our configuration class
    database url and other things here...
    admin:admin123@prudent.cgpamkh0cvsh.us-west-2.rds.amazonaws.com:3306
"""
    ENTRIES_PER_PAGE = 12 #this is the number of records that will be displayed on single page : eg 10 students on one page
    SECRET_KEY = "Asecretkey" # this is the applications secret key
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+os.getenv('RDS_UNAME')+':'+os.getenv('RDS_PWD')+'@'+os.getenv('RDS_URL')+':3306/'+os.getenv('RDS_DB') # DB URL //username:password@address:port/dbname this is the format. 
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/dummy' # DB URL //username:password@address:port/dbname this is the format. 
=======
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+os.getenv('RDS_UNAME')+':'+os.getenv('RDS_PWD')+'@'+os.getenv('RDS_URL')+':3306/'+os.getenv('RDS_DB') # DB URL //username:password@address:port/dbname this is the format. 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/dummy' # DB URL //username:password@address:port/dbname this is the format. 
>>>>>>> 7a8954e41004b681781056842a842a5398a65eb0
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SERVICE_WORKER_PATH = base_dir #this is the service worker by which we get notifications.
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT =  465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'developernil98@gmail.com'#os.getenv('EMAIL')
    MAIL_PASSWORD = 'dattaraj@8101998'#os.getenv('PWD')
    CERT_PATH = base_dir+'/certificate/'

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'test.db')  # + join(_cwd, 'testing.db')
    LIVESERVER_PORT = 0
    MAIL_SUPPRESS_SEND = False
    # Since we want our unit tests to run quickly
    # we turn this down - the hashing is still done
    # but the time-consuming part is left out.
    HASH_ROUNDS = 1