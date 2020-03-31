import os

base_dir = os.path.abspath(os.path.dirname(__file__))
class Config():
    ENTRIES_PER_PAGE = 10
    SECRET_KEY = "Asecretkey"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:nilesh@8101998@localhost:3306/dummy'
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SERVICE_WORKER_PATH = "/media/nilesh/Work/BE Project(Sponsored)/POC Feedback Form/POC"
