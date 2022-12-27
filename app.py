from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

labels = 'Postive', 'Negative', 'Neutral'

st.title("Personality Identifier")

name=st.text_input("Enter the name")

name=name.split()
name="%20".join(name)

name="&q="+name

url="https://newsdata.io/api/2/news?apikey=pub_14912d9a2a9ade17902f701bc34c4cab428e1&language=en"

url=url+name
response=requests.get(url)
df=pd.DataFrame(response.json()['results'])

# print(df.shape[0])

if(df.shape[0]==0):
    st.write("No news were found with the given name")

else:

    df=df[['title','description']]
    analyzer=SentimentIntensityAnalyzer()

    negative=[]
    positive=[]
    neutral=[]

    cnt=0
    df.dropna(inplace=True)
    if(df.shape[0]==0):
        st.write("No news were found with the given name")

    else:
        for i in range(df.shape[0]):
            title=df.iloc[i,0]
            description=df.iloc[i,1]
            title_analyzed=analyzer.polarity_scores(title)
            description_analyzed=analyzer.polarity_scores(description)
            negative.append((title_analyzed['neg']+description_analyzed['neg'])/2)
            positive.append((description_analyzed['pos']+title_analyzed['pos'])/2)
            neutral.append((description_analyzed['neu']+title_analyzed['neu'])/2)
            cnt+=2

        negative_per=sum(negative)*10
        positive_per=sum(positive)*10
        neutral_per=sum(neutral)*10
        rem=100-(negative_per+positive_per+neutral_per)
        st.write("The person is {}% negative".format(negative_per))
        st.write("The person is {}% postive".format(positive_per))
        st.write("The person is {}% neutral".format(neutral_per))
        st.write("{}% is compound news")
        sizes=[]
        sizes.append(negative_per)
        sizes.append(positive_per)
        sizes.append(neutral_per)
        sizes.append(rem)
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

