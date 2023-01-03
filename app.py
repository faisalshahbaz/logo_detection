import streamlit as st
import tweepy
import requests
import numpy as np
from io import BytesIO
from PIL import Image
import cv2
import imutils
from st_aggrid import AgGrid
from yolomodel import model
import pandas as pd
import os

#  streamlit run charlielogo_detection.py --server.fileWatcherType none

consumer_key = 'JLrCWmu0kMWFY9N0q9gAvawRX'
consumer_secret = '1VCj0HZiSzivTgks8mAO5cce0JdMqBJr0toDs4wjGKjwRPYAA4'
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

createdate = []
username = []
tweetsurl = []
imageurl = []


def url_to_numpy(url):
    img = Image.open(BytesIO(requests.get(url).content))
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)


st.title("Demo Project - Logo Detection")

hashtag = st.text_input('Enter your hashtag search from twitter')
tweetcount = st.slider('Tweet count?', 0, 1000, 50)

if st.button('Start Process'):
    st.write("Tweet Extraction.....")
    my_bar = st.progress(0)
    try:
        tweets = tweepy.Cursor(api.search_tweets,
                               "#" + str(hashtag), lang="en",
                               tweet_mode='extended').items(int(tweetcount))

        for tweet in tweets:
            if tweet.entities['user_mentions'] and "media" in tweet.entities:
                if tweet.entities['media'][0]['type'] == 'photo':
                    createdate.append(tweet.created_at)
                    username.append(tweet.entities['user_mentions'][0]['screen_name'])
                    tweetsurl.append(tweet.entities['media'][0]['expanded_url'])
                    imageurl.append(tweet.entities['media'][0]['media_url'])
            else:
                continue

        my_bar.progress(100)

    except:
        st.error("no tweet found", icon="🤖")

    listdate = []
    listuser = []
    listurl = []
    listimg = []

    st.write("Logo Detection Processing ....")
    my_bar1 = st.progress(0)

    for date, user, url, imgurl in zip(createdate, username, tweetsurl, imageurl):
        img = url_to_numpy(imgurl)
        if img is not None:
            frame = imutils.resize(img, width=1280)
            results = model([frame], size=1280)

            if results.pandas().xyxy[0].empty is not True:
                listdate.append(date)
                listuser.append(user)
                listurl.append(url)
                listimg.append(imgurl)

    my_bar1.progress(100)
    st.write(os.path.dirname('image1.jpg'))
    data = {
        "CreatedAt": listdate,
        "UserName": listuser,
        "TweetURL": listurl,
        "TweetImage": listimg
    }

    df = pd.DataFrame(data)
    AgGrid(df)
    st.balloons()
