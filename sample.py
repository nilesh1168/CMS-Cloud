import pandas as pd 
import numpy as np
from POC import db
from POC.models import Session, Feedback, Response
query = db.session.query(Feedback.mobile, Feedback.sentiment, Response.answer).filter(Feedback.mobile == Response.stud_mobile).all()
print(type(query))
df = pd.DataFrame(query,columns=['Mobile no','Sentiment','Answer'])
df[['Answer1','Answer2','Answer3','Answer4','Answer5']] = df.Answer.str.split(",",expand=True,)
df.loc[df['Sentiment'] == 'POSITIVE','Sentiment'] = 1 
df.loc[df['Sentiment'] == 'NEGATIVE','Sentiment'] = 0 
df.loc[df['Answer1'] == 'YES','Answer1'] = 1 
df.loc[df['Answer1'] == 'NO','Answer1'] = 0 
df.loc[df['Answer2'] == 'YES','Answer2'] = 1 
df.loc[df['Answer2'] == 'NO','Answer2'] = 0 
df.loc[df['Answer3'] == 'YES','Answer3'] = 1 
df.loc[df['Answer3'] == 'NO','Answer3'] = 0 
df.loc[df['Answer4'] == 'YES','Answer4'] = 1 
df.loc[df['Answer4'] == 'NO','Answer4'] = 0 
df.loc[df['Answer5'] == 'YES','Answer5'] = 1 
df.loc[df['Answer5'] == 'NO','Answer5'] = 0  
df.drop(["Answer"], axis = 1, inplace = True) 
print(df)
df.to_csv('C:/Users/Aniket Pawar/Desktop/anuja.csv')
