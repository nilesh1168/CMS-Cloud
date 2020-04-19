import pandas as pd 
import numpy as np
from POC import db
from POC.models import Session, Feedback, Response
query = db.session.query(Feedback.mobile, Feedback.sentiment, Response.answer).filter(Feedback.mobile == Response.stud_mobile).all()
print(type(query))
df = pd.DataFrame(query,columns=['Mobile no','Sentiment','Answer'])
df[['Answer1','Answer2','Answer3','Answer4','Answer5']] = df.Answer.str.split(",",expand=True,)
df.drop(["Answer"], axis = 1, inplace = True) 
print(df.dtypes)
# df.to_csv('/home/nilesh/Desktop/test.csv')
