from POC import db,app
from POC.models import Session
sessions = Session.query.paginate(1,app.config['ENTRIES_PER_PAGE'],False)
print(sessions);