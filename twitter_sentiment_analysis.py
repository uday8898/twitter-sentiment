import streamlit as st
import tweepy
from textblob import TextBlob
import pandas as pd

# Set up Twitter API credentials
API_KEY = 'aunIg4HcrcilMtAfffQdW1BYW'
API_SECRET_KEY = '266jLR4esR0Zn9yrr2aU2HtyPAOCIJLoxliuXDGcpgzEubbDto'
ACCESS_TOKEN = '1263007663291371520-MXjEzr16cpEDbu5Ps6FTbvcsOIpIKu'
ACCESS_TOKEN_SECRET = 'bWw4kmIAnnyAls4oUKJem0fD3tQ6QMoAyyvrhjmedsycC'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to fetch tweets
def fetch_tweets(query, count=100):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en').items(count)
    tweets_list = [[tweet.text, tweet.created_at, tweet.user.screen_name] for tweet in tweets]
    return tweets_list

# Function to analyze sentiment
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Streamlit app
st.title("Twitter Sentiment Analysis")

query = st.text_input("Enter the keyword/hashtag to search for:", "Streamlit")
count = st.slider("Number of tweets to fetch:", 10, 200, 50)

if st.button("Fetch Tweets"):
    with st.spinner("Fetching tweets..."):
        tweets = fetch_tweets(query, count)
        df = pd.DataFrame(tweets, columns=['Tweet', 'Date', 'User'])
        df['Sentiment'] = df['Tweet'].apply(analyze_sentiment)

        st.success("Tweets fetched successfully!")
        st.write(df)

        sentiment_count = df['Sentiment'].value_counts()
        st.bar_chart(sentiment_count)
