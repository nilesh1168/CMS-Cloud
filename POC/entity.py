class feedbackEntity:
    answer = None
    session = None
    def __init__(self,answer,session):
        self.answer = answer
        self.session = session

    def getSession(self):
        return self.session    

    def getAnswers(self):
        return self.answer    