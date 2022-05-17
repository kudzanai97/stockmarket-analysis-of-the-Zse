import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import investpy as inv
from bs4 import BeautifulSoup as bs
import requests
from textblob import TextBlob
from urllib.request import urlopen, Request
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import streamlit as st
import re 
import sys
import tweepy 
from tweepy import OAuthHandler 
import warnings
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Tanaka neMusika", page_icon=":tada:", layout="wide")

st.title("Tanaka's stock forecaster ")
st.subheader("This app is not foolproof and it is not to be relied upon 100% when investing your money on the ZSE. At most it can only serve as a guide the honours is on you to do an extensive research before taking a position on an counter")
with st.form(key="my_form",clear_on_submit= True):
    userInput= st.text_input("enter stock ticker eg ECO")
    submit_button= st.form_submit_button("enter")
    if submit_button:
        #userInput= st.input("enter stock ticker")
        start= '2021-01-01'
        end= '2022-o4-01'

        with st.container():

            #getting the stock data
            st.write("---")
            leftC, rightC = st.columns(2)
            
            try:
                with leftC:
                    
                    infor= inv.get_stock_company_profile(stock=userInput, country="Zimbabwe")
                    df = inv.get_stock_historical_data(stock=userInput,
                                                country="Zimbabwe",
                                                from_date="01/01/2019",
                                                to_date="05/05/2022")

                    
                    ku = inv.get_stock_historical_data(stock=userInput,
                                                country="Zimbabwe",
                                                from_date="01/03/2022",
                                                to_date="14/03/2022")
                    print(infor)
                    print(df.head())
                    print(ku.head())
                    st.header("Company profile")
                    st.write("##")
                    st.write(infor)
                with rightC:
                    st.header("Stock historical data")
                    st.write(df.head())
            except:
                st.write("failed to connect check your connection and if your stock ticker is correct")
                sys.exit(1)
                
        #get the close column price

        df= df[['Close']]
        forecast= 30 #the predictor variable
        #create the dependent variable
        df['Prediction']= df[['Close']].shift(-forecast)
        ku= ku[['Close']]

        #create the independent data set
        x= np.array(df.drop(['Prediction'],1))
        q= np.array(ku['Close'])
        #remove the last forecast roles
        x= x[:-forecast]
        #create the dependent dataset
        y= np.array(df['Prediction'])
        y= y[:-forecast]
        #split the data into 80%training testing
        xtrain,xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2)
        #create and train the SVM
        svr= SVR(kernel='rbf', C=1e3, gamma=0.1)

        svr.fit(xtrain, ytrain)
        with st.container():

            #testing model
            #svm regressor model
            svmConfidence= svr.score(xtest, ytest)
            print('svm confidence', svmConfidence)
            #predictions
            xForecast= np.array(df.drop(['Prediction'],1))[-forecast:]

            prediction= svr.predict(xForecast)
            st.subheader("Forecasted stock trend")
            st.write('a confidence level' ,svmConfidence)
            fig =plt.figure(figsize=(12,6))
            plt.plot(prediction, 'r', label='predicted price')
            plt.xlabel('time')
            plt.ylabel('price')
            plt.legend()
            st.pyplot(fig)
        score= 0
        st.header('FUNDAMENTAL ANALYSIS (The Piotroski f-score)')
        st.write("##")
        st.write("The Piotroski score is a discrete score between zero and nine that reflects nine criteria used to determine the strength of a firm's financial position. The Piotroski score is used to determine the best value stocks, with nine being the best and zero being the worst")
        st.write("data supplied by Tanaka Chabara a financial enthusiastic")
        st.write("##")
        if userInput=="ECO":
            st.subheader("The company has the Piotroski score of 8")
            score= 8
        elif userInput== "OKZ":
            st.subheader("The company has the Piotroski score of 4")
            score=4
        elif userInput== "ASUN":
            st.subheader("The company has the Piotroski score of 3")
            score= 3
        elif userInput== "AFDS":
            st.subheader("The company has the Piotroski score of 5")
            score=5
        elif userInput== "BAT":
            st.subheader("The company has the Piotroski score of 8")
            score=8
        elif userInput== "BRDR":
            st.subheader("The company has the Piotroski score of 2")
            score=2
        elif userInput== "CAFCA":
            st.subheader("The company has the Piotroski score of 7")
            score=7
        elif userInput== "CBZ":
            st.subheader("The company has the Piotroski score of 6")
            score=6
        elif userInput== "DLTA":
            st.subheader("The company has the Piotroski score of 8")
            score=8
        elif userInput== "EDGR":
            st.subheader("The company has the Piotroski score of 3")
            score=3
        elif userInput== "FBC":
            st.subheader("The company has the Piotroski score of 4")
            score=4
        elif userInput== "GBZW":
            st.subheader("The company has the Piotroski score of 1")
            score=1
        elif userInput== "HIPO":
            st.subheader("The company has the Piotroski score of 7")
            score=7
        elif userInput== "INN":
            st.subheader("The company has the Piotroski score of 8")
            score=8
        elif userInput== "LACZ":
            st.subheader("The company has the Piotroski score of 5")
            score=5
        elif userInput== "MASH":
            st.subheader("The company has the Piotroski score of 6")
            score=6
        elif userInput== "MSHL":
            st.subheader("The company has the Piotroski score of 3")
            score=3
        elif userInput== "NPKZ":
            st.subheader("The company has the Piotroski score of 3")
            score=3
        elif userInput== "RIOZ":
            st.subheader("The company has the Piotroski score of 5")
            score=5
        elif userInput== "SEED":
            st.subheader("The company has the Piotroski score of 6")
            score=6
        elif userInput== "SIM":
            st.subheader("The company has the Piotroski score of 6")
            score=6
        elif userInput== "TANG":
            st.subheader("The company has the Piotroski score of 7")
            score=7
        elif userInput== "TRUW":
            st.subheader("The company has the Piotroski score of 3")
            score=3
        elif userInput== "TSL":
            st.subheader("The company has the Piotroski score of 4")
            score=4
        elif userInput== "UNIF":
            st.subheader("The company has the Piotroski score of 5")
            score=5
        elif userInput== "ZIMP":
            st.subheader("The company has the Piotroski score of 3")
            score=3
        elif userInput== "ZIMW":
            st.subheader("The company has the Piotroski score of 5")
            score=5
        elif userInput== "SACL":
            st.subheader("The company has the Piotroski score of 3")
            score=3
        elif userInput== "RTG":
            st.subheader("The company has the Piotroski score of 5")
            score=5
        elif userInput== "OMU":
            st.subheader("The company has the Piotroski score of 5")
            score=5
        elif userInput== "NTS":
            st.subheader("The company has the Piotroski score of 6")
            score=6
        elif userInput== "NTFD":
            st.subheader("The company has the Piotroski score of 6")
            score=6
        elif userInput== "DZL":
            st.subheader("The company has the Piotroski score of 5")
            score=5
        elif userInput== "EHZL":
            st.subheader("The company has the Piotroski score of 6")
            score=6
        else:
            st.subheader("Not enough data ")
            score= 10

###SEntimental analysis
        
        url1= "https://www.fingaz.co.zw/category/c77-companies-a-markets/"
        url2= "https://businesstimes.co.zw/category/markets/"
        req= Request(url=url1, headers={'user-agent': 'myApp'})
        response= urlopen(req)
        html= bs(response, 'html.parser')
        title= []
        newslist=[]
    #newsList= html.find('article')
        newsList= html.find(id="headermenu")
        newsdata= newsList.findAll('h6')
        for index, row in enumerate(newsdata):
            ti= row.a.text
            title.append(ti)
        data= pd.DataFrame(title, columns=['headlines'])
        i=0
        negative=0
        positive=0
        neutral=0
        while i< len(data):
            sentence = title[i]
            Polarity= TextBlob(sentence).polarity
            if Polarity== 0:
                neutral= neutral +1
            elif Polarity> 0:
                positive= positive+1
            else:
                negative=negative+1
            i=i+1
        sentiment=[positive, negative, neutral]
        Labels= ['Positive', 'Negative', 'Neutral']
        from matplotlib import pyplot as plt
        fig3= plt.figure(figsize= (1,1))
        st.subheader("some of the news headlines")
        st.write(data.head())
        plt.title("The Results of the sentimental analysis of news") 
        plt.pie(sentiment, labels= Labels)
        st.pyplot(fig3)
        if positive> negative:
            if score==10:
                st.write("there was not enough information to have a position on this counter ")
            elif score>6:
                st.write("the general sentiments are more positive and its f-score is good it might be a great add to your portfolio in the long run  ")
            elif score>3:
                st.write("its a good counter with lots of potential and with the positve aura available u may take a position")
            else:
                st.write("a poorly performing counter not applicable for position trading ")
        else:
            if score==10:
                st.write("there was not enough information to have a position on this counter ")
            elif score>6:
                st.write("the general sentiments are more negative but its f-score is good and these counters are usualy the safer bets  ")
            elif score>3:
                st.write("its a good counter with lots of potential but with the negative aura available u may take a wait and see approach")
            else:
                st.write("a poorly performing counter not applicable for position trading ")

        
            #SENTIMENTAL ANALYSIS
        class TwitterClient(object):
                def __init__(self):
                    
                    consumer_key = 'EwG6T8KZTCuSfv6Wy2rfUu1gO' 
                    consumer_secret = 'R8dREd4HyxY6flL3OOHktuEfkTAXj66HZ5QGWGUsmoKfcaNhND'
                    access_token = '405461195-HdMbZqc7YmMP5yTMG5rix5nrahxGP72WG9VjF6w1'
                    access_token_secret = '9Zl6g93TtRvH3voFlOd6pbDwFGZ5A7YLDJnogrkm1O0NT'
                    try:
                        self.auth= OAuthHandler(consumer_key, consumer_secret)
                        self.auth.set_access_token(access_token, access_token_secret)
                        self.api = tweepy.API(self.auth)
                    except:
                        print("Error: Authentication Failed")
                def clean_tweet(self, tweet):
                    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
                def get_tweet_sentiment(self, tweet):
                    analysis= TextBlob(self.clean_tweet(tweet))
                    if analysis.sentiment.polarity > 0:
                        return "positive"
                    elif analysis.sentiment.polarity == 0:
                        return "neutral"
                    else:
                        return "negative"
                def get_tweets(self, query, count =10):
                    tweets=[]
                    try:
                        fetched_tweets= self.api.search(q= query, count= count)
                        for tweet in fetched_tweets:
                            parsed_tweet={}
                            parsed_tweet['text']= tweet.text
                            parsed_tweet['sentiment']= self.get_tweet_sentiment(tweet.text)
                            if tweet.retweet_count>0:
                                if parsed_tweet not in tweets:
                                    tweets.append(parsed_tweet)
                            else:
                                tweets.append(parsed_tweet)
                        return tweets
                    except tweepy.TweepError as e:
                        print("Error: "+ str(e))
                def main():
                    api= TwitterClient()
                    tweets= api.get_tweets(query ='ZSE', count= 100)
                    #ptweets = == 'positive'
                    #x = print("positive tweets percentage: {}%".format(100*len(ptweets)/len(tweets)))
                    
                    #ntweets= == 'negative'
                    #y = print("negative tweets percentage: {}%".format(100*len(ntweets)/len(tweets)))
                #if __name__=="__main__":
                    #main()
        #st.write("the general sentiment on twitter is positive implying the market will go up") 
                        
                