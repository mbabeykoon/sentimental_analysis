# #NFT and Sentiment Analysis on Twitter data
We'll use Twitter API with the tweepy python library to fetch Twitter tweets in this project. We'll apply various data engineering skills to analyze  Twitter data. 
We'll follow these three major steps in our program in this project:
    1)Authorize Twitter API client.
    2)Make a GET request to Twitter API to fetch tweets for a particular query.
    3)Classify each tweet as positive, negative, or neutral.
Also, we create a Sentiment Analysis scatter plot, Sentiment Analysis bar plot, and word cloud for query "#minority."

![Screenshot](wordCloud.png)


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file.
You can get following veribles by sign up for Twitter developer account. Insert your credentials instead of 'xxxxx' .
consumer_key= 'xxxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxxxxxx'
access_token_secret = 'xxxxxxxxxxxxxxxxxxxx'


## Prerequisites

All the required packages and libraries are listed in file requirements.txt. They can be installed in venv using pip install requirements.txt.