import pandas as pd
from sqlalchemy import create_engine, text
import nltk
#import psycopg2
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env file into the environment
passw = os.getenv('PASSWORD')
user=os.getenv('USER')


nltk.download('vader_lexicon')

def fetch_data_from_sql():

    engine = create_engine(f"postgresql://{user}:{passw}@localhost:5433/Marketing_Analytics")
    query='''SELECT 
    "ReviewID",
    "CustomerID",
    "ProductID",
    "ReviewDate",
    "Rating",
    REPLACE("ReviewText", '  ', ' ') AS "ReviewText"
     FROM 
    customer_reviews;
                   '''
    df1 = pd.read_sql(query, engine)

    #print(df.head())
    return df1

sia=SentimentIntensityAnalyzer()

def calculate_sentiment(reviews):
    score=sia.polarity_scores(reviews)
    return score['compound']

def categorize_sentiment(score,rating):
    if score>0.05:
        if rating>3:
            return "Positive"
        elif rating==3:
            return "Mixed Positive"
        else:
            return "Mixed Negative"
    elif score<-0.05:
        if rating>3:
            return "Mixed Positive"
        elif rating<3:
            return "Negative"
        elif rating==3:
            return "Mixed Negative"
    else:
        if rating>3:
            return "Positive"
        elif rating<3:
            return "Negative"
        else:
            return "Neutral"

def sentiment_score_bucket(score):
    if score>0.5:
        return '0.5 to 1' #strong pos
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'  # Mild pos
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'  # Mild neg
    else:
        return '-1.0 to -0.5' #strong neg




if __name__=='__main__':
    df=fetch_data_from_sql()
    #calculate_sentiment(df['ReviewText'][2])
    df['SentimentScore'] = df['ReviewText'].apply(calculate_sentiment) #find score first
    df['SentimentCategory']= df.apply(lambda row: categorize_sentiment(row['SentimentScore'],row['Rating']),axis=1) #applied sentiment catgeory

    df['SentimentBucket']=df['SentimentScore'].apply(sentiment_score_bucket)

    print(df.head())
    df.to_csv("customer_review_enriched.csv",index=False)