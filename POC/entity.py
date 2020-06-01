from POC.models import Session
class feedbackEntity:
    answer = None
    session = Session()
    def __init__(self,answer,session):
        self.answer = answer
        self.session = session