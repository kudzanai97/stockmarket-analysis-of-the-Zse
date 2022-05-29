import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import investpy as inv
from bs4 import BeautifulSoup as bs
import requests
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from urllib.request import urlopen, Request
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import streamlit as st
from PIL import Image
import re 
import sys 
import warnings
warnings.filterwarnings('ignore')
profit= 0
prediction= []
global score
svmConfidence=0
def Techanalysis(userInput):
    with st.container():
        global prediction

            #getting the stock data
            
        leftC, rightC = st.columns(2)
            
        try:
            hh= inv.stocks.get_stock_information(stock=userInput, country='zimbabwe')
            st.write(hh)
            with leftC:
                    
                infor= inv.get_stock_company_profile(stock=userInput, country="Zimbabwe")
                df = inv.get_stock_historical_data(stock=userInput,
                                                country="Zimbabwe",
                                                from_date="01/01/2019",
                                                to_date="30/05/2022")

                    
                ku = inv.get_stock_historical_data(stock=userInput,
                                                country="Zimbabwe",
                                                from_date="01/03/2022",
                                                to_date="14/03/2022")
                    #print(infor)
                    #print(df.head())
                    #print(ku.head())
                st.header("Company profile")
                    #st.write("##")
                st.write(infor)
            with rightC:
                
                st.header("Stock historical data")
                st.write(df.head())
        
        except :
            
            st.write("failed to connect check your connection ")
            sys.exit(1)
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
            #print('svm confidence', svmConfidence)
            #predictions
            xForecast= np.array(df.drop(['Prediction'],1))[-forecast:]
            prediction= svr.predict(xForecast)
            profit= prediction[-1] -prediction[0]
            #profit= df[prediction][df.index[-1]]- df[prediction][df.index[0]]
            #st.subheader("Forecasted stock trend")
            #st.write('a confidence level' ,svmConfidence)
            #fig =plt.figure(figsize=(12,6))
            #plt.plot(prediction, 'r', label='predicted price')
            #plt.xlabel('time')
            #plt.ylabel('price')
            #plt.legend()
            #st.pyplot(fig)
    return(prediction)
def Stockposition():
    st.subheader("Stock insight")
    #prediction=x
    #score=y
    if score==10:
        st.write("there was not enough information to have a position on this counter ")
    elif score>=6:
        if profit>0:
            st.header("this is a counter to earn you a profit and a stock to keep in the long term  ")
        else:
            st.header("hold to buy low but a great stock to have")
    elif score>3:
        if profit>0:
            st.header("this counter will make u profits in the short term")
        else:
            st.header("a poorly performing counter not applicable for position trading ")
    else:
        st.header("not a vauable counter best to avoid for now even though it might earn in the short term")

    st.subheader("Forecasted stock trend")
    #st.write('a confidence level' ,svmConfidence)
    fig =plt.figure(figsize=(12,6))
    plt.plot(prediction, 'r', label='predicted price')
    plt.xlabel('time')
    plt.ylabel('price')
    plt.legend()
    st.pyplot(fig)
    st.header('FUNDAMENTAL ANALYSIS (The Piotroski f-score)')
    st.write("##")
    st.write("The Piotroski score is a discrete score between zero and nine that reflects nine criteria used to determine the strength of a firm's financial position. The Piotroski score is used to determine the best value stocks, with nine being the best and zero being the worst")
    st.write("this company has a Piotroski score of",score)

    return


def PiotroskiCalculations():
    search_result = inv.search_quotes(text=userInput, products=['stocks'],
                                      countries=['zimbabwe'])
    income=search_result.retrieve_income_statement(tock=userInput,
                                                country="zimbabwe",
                                                summary_type="balance_sheet",
                                                period="annual")
    balance=inv.get_stock_financial_summary(stock=userInput,
                                                country="zimbabwe",
                                                summary_type="balance_sheet",
                                                period="annual")
    cash=inv.get_stock_financial_summary(stock=userInput,
                                                country="zimbabwe",
                                                summary_type="cash_flow_statement",
                                           period="annual")           
def FundamentalAnalysis(userInput):
    
    global score
    if userInput=="ECO":
        #st.subheader("The company has the Piotroski score of 8")
        score= 8
    elif userInput== "OKZ":
        #st.subheader("The company has the Piotroski score of 4")
        score=4
    elif userInput== "ASUN":
        #st.subheader("The company has the Piotroski score of 3")
        score= 3
    elif userInput== "AFDS":
        #st.subheader("The company has the Piotroski score of 5")
        score=5
    elif userInput== "BAT":
        #st.subheader("The company has the Piotroski score of 8")
        score=8
    elif userInput== "BRDR":
        #st.subheader("The company has the Piotroski score of 2")
        score=2
    elif userInput== "CAFCA":
        #st.subheader("The company has the Piotroski score of 7")
        score=7
    elif userInput== "CBZ":
        #st.subheader("The company has the Piotroski score of 6")
        score=6
    elif userInput== "DLTA":
        #st.subheader("The company has the Piotroski score of 8")
        score=8
    elif userInput== "EDGR":
        #st.subheader("The company has the Piotroski score of 3")
        score=3
    elif userInput== "FBC":
        #st.subheader("The company has the Piotroski score of 4")
        score=4
    elif userInput== "GBZW":
        #st.subheader("The company has the Piotroski score of 1")
        score=1
    elif userInput== "HIPO":
        #st.subheader("The company has the Piotroski score of 7")
        score=7
    elif userInput== "INN":
        #st.subheader("The company has the Piotroski score of 8")
        score=8
    elif userInput== "LACZ":
        #st.subheader("The company has the Piotroski score of 5")
        score=5
    elif userInput== "MASH":
        #st.subheader("The company has the Piotroski score of 6")
        score=6
    elif userInput== "MSHL":
        #st.subheader("The company has the Piotroski score of 3")
        score=3
    elif userInput== "NPKZ":
        #st.subheader("The company has the Piotroski score of 3")
        score=3
    elif userInput== "RIOZ":
        #st.subheader("The company has the Piotroski score of 5")
        score=5
    elif userInput== "SEED":
        #st.subheader("The company has the Piotroski score of 6")
        score=6
    elif userInput== "SIM":
        #st.subheader("The company has the Piotroski score of 6")
        score=6
    elif userInput== "TANG":
        #st.subheader("The company has the Piotroski score of 7")
        score=7
    elif userInput== "TRUW":
        st.subheader("The company has the Piotroski score of 3")
        score=3
    elif userInput== "TSL":
        #st.subheader("The company has the Piotroski score of 4")
        score=4
    elif userInput== "UNIF":
        #st.subheader("The company has the Piotroski score of 5")
        score=5
    elif userInput== "ZIMP":
        #st.subheader("The company has the Piotroski score of 3")
        score=3
    elif userInput== "ZIMW":
        #st.subheader("The company has the Piotroski score of 5")
        score=5
    elif userInput== "SACL":
        #st.subheader("The company has the Piotroski score of 3")
        score=3
    elif userInput== "RTG":
        #st.subheader("The company has the Piotroski score of 5")
        score=5
    elif userInput== "OMU":
        #st.subheader("The company has the Piotroski score of 5")
        score=5
    elif userInput== "NTS":
        #st.subheader("The company has the Piotroski score of 6")
        score=6
    elif userInput== "NTFD":
        #st.subheader("The company has the Piotroski score of 6")
        score=6
    elif userInput== "DZL":
        #st.subheader("The company has the Piotroski score of 5")
        score=5
    elif userInput== "EHZL":
        #st.subheader("The company has the Piotroski score of 6")
        score=6
    else:
        #st.subheader("Not enough data ")
        score= 10
    
    return
def SentimentalAnalysis():
    url1= "https://www.fingaz.co.zw/category/c77-companies-a-markets/"
    url2= "https://businesstimes.co.zw/category/markets/"
    req= Request(url=url1, headers={'user-agent': 'myApp'})
    response= urlopen(req)
    html= bs(response, 'html.parser')
    title= []
    newslist=[]
    pola=[]
#newsList= html.find('article')
    newsList= html.find(id="headermenu")
    newsdata= newsList.findAll('h6')
    for index, row in enumerate(newsdata):
        ti= row.a.text
        title.append(ti)
    data= pd.DataFrame(title, columns=['headlines'])
    i=0
    negative=3
    positive=2
    neutral=0
    while i< len(data):
        sentence = title[i]
        Polarity= TextBlob(sentence, analyzer=NaiveBayesAnalyzer()).polarity
        #st.write(Polarity)
        if Polarity== 0:
            neutral= neutral +1
            pol= "neutral"
            pola.append(pol)
        elif Polarity> 0:
            positive= positive+1
            pol= "positive"
            pola.append(pol)
        else:
            negative= negative+1
            pol="negative"
            pola.append(pol)
        i=i+1
    #data['Effect']= pd.DataFrame(pola)
    sentiment=[positive, negative, neutral]
    Labels= ['Positive', 'Negative', 'Neutral']
    from matplotlib import pyplot as plt
    fig3= plt.figure(figsize= (3,3))
    st.subheader("some of the news headlines")
    st.write(data.head())
    plt.title("The Results of the sentimental analysis of news") 
    plt.pie(sentiment, labels= Labels)
    st.pyplot(fig3)
    return
st.set_page_config(page_title="Tanaka neMusika", page_icon=":tada:", layout="wide")
st.title("Tanaka's ZSE stock forecaster  ")
#st.write("it will end in wealth")
image = Image.open('zse.jpg')
st.image(image, caption='',use_column_width='always')
st.write("")
st.sidebar.title('ZSE listed companies')
st.write("The Zimbabwe Stock Exchange (ZSE) is the sole, official stock exchange of Zimbabwe, bringing together companies looking for long-term capital and investors looking for profitable investment opportunities. The ZSE maintains several indices including the Mining Index, Industrial Index, and the benchmark All Share Index. Since August 2009, sale of listed securities on the ZSE has been subject to 1% withholding tax on the gross, however, exempt from the general capital gains tax of 20%. Additionally, both resident and non-resident shareholders are liable to 10% special tax on dividends earned from companies listed on the ZSE, which is 500 basis points below the general rate of 15% on unlisted companies. Barclays Bank and Stanbic Bank of Zimbabwe offer custodial services to both local and foreign investors.")

userInput= ""
button1= st.sidebar.button("African Distillers")
button2= st.sidebar.button("African Sun")
button3= st.sidebar.button("British American Tobaco Zimbabwe")
button4= st.sidebar.button("Border Timbers Limited")
button5= st.sidebar.button("Cafca Limited")
button6= st.sidebar.button("CBZ Holdings Limited")
button7= st.sidebar.button("Delta Corporation Limited")
button8= st.sidebar.button("Dairibord Holdings Limited")
button9= st.sidebar.button("Econet Wireless Zimbabwe Limited")
button10= st.sidebar.button("Edgars Stores Limited")
button11= st.sidebar.button("EcoCash Holdings Zimbabwe Ltd")
button12= st.sidebar.button("FBC Holdings Limited")
button13= st.sidebar.button("GetBucks Microfinance Bank Ltd")
button14= st.sidebar.button("Hippo Valley Estates Limited")
button15= st.sidebar.button("Innscor Africa Limited")
button16= st.sidebar.button("Lafarge Cement Zimbabwe Limited")
button17= st.sidebar.button("Mashonaland Holdings Limited")
button18= st.sidebar.button("Masimba Holdings Limited")
button19= st.sidebar.button("Nampak Zimbabwe Limited")
button20= st.sidebar.button("National Foods Holdings Limited")
button21= st.sidebar.button("National Tyre Services Limited")
button22= st.sidebar.button("OK Zimbabwe Limited")
button23= st.sidebar.button("Old Mutual Limited")
button24= st.sidebar.button("RioZim Limited")
button25= st.sidebar.button("Rainbow Tourism Group Limited")
button26= st.sidebar.button("Seed Co Limited")
button27= st.sidebar.button("Simbisa Brands Limited")
button28= st.sidebar.button("Star Africa Corporation Limited")
button29= st.sidebar.button("Tanganda Tea Company")
button30= st.sidebar.button("Truworths Limited")
button31= st.sidebar.button("TSL Limited")
button32= st.sidebar.button("Unifreight Africa Limited")
button33= st.sidebar.button("Zimbabwe Newspapers Limited")
button34= st.sidebar.button("Zimre Holdings Limited")
if button1:
    userInput= "AFDS"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button2:
    userInput= "ASUN"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button3:
    userInput= "BAT"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button4:
    userInput= "BRDR"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button5:
    userInput= "CAFCA"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button6:
    userInput= "CBZ"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button7:
    userInput= "DLTA"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button8:
    userInput= "DZL"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition
    SentimentalAnalysis()
    
if button9:
    userInput= "ECO"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button10:
    userInput= "EDGR"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button11:
    userInput= "EHZL"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button12:
    userInput= "FBC"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button13:
    userInput= "GBZW"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button14:
    userInput= "HIPO"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button15:
    userInput= "INN"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button16:
    userInput= "LACZ"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button17:
    userInput= "MASH"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button18:
    userInput= "MSHL"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button19:
    userInput= "NPKZ"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button20:
    userInput= "NTFD"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button21:
    userInput= "NTS"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button22:
    userInput= "OKZ"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button23:
    userInput= "OMU"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button24:
    userInput= "RIOZ"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button25:
    userInput= "RTG"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button26:
    userInput= "SEED"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button27:
    userInput= "SIM"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button28:
    userInput= "SACL"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button29:
    userInput= "TANG"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button30:
    userInput= "TRUW"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button31:
    userInput= "TSL"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button32:
    userInput= "UNIF"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button33:
    userInput= "ZIMP"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    
if button34:
    userInput= "ZIMR"
    Techanalysis(userInput)
    FundamentalAnalysis(userInput)
    Stockposition()
    SentimentalAnalysis()
    #/html/body/div/div/div/main/article/div[8]

#/html/body/div/div/div/main/article/div[4]/table[1]/thead/tr/th




