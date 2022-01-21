# import the libararies
import os
import tweepy
import pandas as pd
import numpy as np
import wordcloud
import re
import matplotlib.pyplot as plt

#------------------------------------------------------------------------#

#import twitter loging credentials
log = pd.read_csv(r'D:\Intern\MP\token.csv')

#twitter credentials
consumer_key= log['key'][0]
consumer_secret = log['key'][1]
access_token = log['key'][2]
access_token_secret = log['key'][3]

#------------------------------------------------------------------------#

# cerate API object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#------------------------------------------------------------------------#

#fectch tweets using query
query = "#minority -filter:retweets"
# get tweets from the API
tweets = tweepy.Cursor(api.search_tweets,
              q=query,
              lang="en",
              since="2017-01-01").items(1000)
# store the API responses in a list
tweets_copy = []
for tweet in tweets:
    tweets_copy.append(tweet)
    
print("Total Tweets fetched:", len(tweets_copy))

#------------------------------------------------------------------------#

# intialize the dataframe
df = pd.DataFrame()
# populate the dataframe
for tweet in tweets_copy:
    hashtags = []
    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
        text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
    except:
        pass
    df = df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,\
                                               'user_description': tweet.user.description,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source}))
    df = df.reset_index(drop=True)
# drop null values
df = df.dropna()

#------------------------------------------------------------------------#

#function to choose twitters with specific hashtags
def search(list):
    for i in range(len(list)):
        if list[i] == 'minority':
          mino = 'minority'
          
            
        else:
          mino = 'other'
    return mino

df['mino'] = df['hashtags'].apply(lambda x: search(x))

#------------------------------------------------------------------------#

#filter dataframe that contain specific hashtag
df = df[df['mino']== 'minority']

#------------------------------------------------------------------------#

# function to clean twitters
def cleanTxt(text):
  text = re.sub(r'@[A-Za-z0-9]+','',text) #Remove @mentiontions
  text = re.sub(r'#','',text) #Remove '#' 
  text = re.sub(r'RT[\s]+','',text) # Remove RT
  text = re.sub(r'https?:\/\/\S+','',text) # Remove the hyper link
  text = re.sub(r'\\n','',text)
  return text

df['text']= df['text'].apply(cleanTxt)

#------------------------------------------------------------------------#

#create subjectivity and polarity columns
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
  return TextBlob(text).sentiment.polarity
df['Subjectivity'] = df['text'].apply(getSubjectivity)
df['Polarity'] = df['text'].apply(getPolarity) 
#------------------------------------------------------------------------#
#create a function to get the sentiment text
def getSentiment(score):
  if score <0:
    return 'Negative'
  elif score ==0:
    return 'Neutral'
  else:
    return 'Positive'

df['Sentiment'] = df['Polarity'].apply(getSentiment)

#------------------------------------------------------------------------#
#create a scatter to show the subjectivity and the polarity
plt.figure(figsize=(8,6))

plt.scatter(df['Polarity'],df['Subjectivity'],color='Purple')
plt.title('Sentiment Analysis Scatter Plot')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

#------------------------------------------------------------------------#
#create a bar chart to show sentiments
df['Sentiment'].value_counts().plot(kind='bar')
plt.title('Sentiment Analysis Bar Plot')
plt.xlabel('Sentiment')
plt.ylabel('Number of tweets')
plt.show()

#------------------------------------------------------------------------#
#Plot the word Cloud
from wordcloud import WordCloud
allWords = ''.join([twts for twts in df['text']])
wordcloud = WordCloud(width=500,height=300,max_font_size=119).generate(allWords)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()