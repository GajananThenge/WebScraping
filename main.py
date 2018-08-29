# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 21:36:34 2018

@author: hp-pc
"""

# script to scrape tweets by a twitter user.
# Author - ThePythonDjango.Com
# dependencies - BeautifulSoup, requests
 
from bs4 import BeautifulSoup
import requests
import sys
import json
 
 
def usage():
    msg = """
    Please use the below command to use the script.
    python script_name.py twitter_username
    """
    print(msg)
    sys.exit(1)
 
 
#def get_username():
#    # if username is not passed
#    if len(sys.argv) < 2:
#        usage()
#    username = sys.argv[1].strip().lower()
#    if not username:
#        usage()
# 
#    return username

def get_tweet_text(tweet):
    tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    images_in_tweet_tag = tweet_text_box.find_all("a", {"class": "twitter-timeline-link u-hidden"})
    tweet_text = tweet_text_box.text
    for image_in_tweet_tag in images_in_tweet_tag:
        tweet_text = tweet_text.replace(image_in_tweet_tag.text, '')
    return tweet_text


def get_this_page_tweets(soup):
    tweets_list = list()
    tweets = soup.find_all("li", {"div": "content"}) #Gives the description
    for tweet in tweets:
        tweet_data = None
        try:
            tweet_data = get_tweet_text(tweet)
        except Exception as e:
            continue
            #ignore if there is any loading or tweet error
 
        if tweet_data:
            tweets_list.append(tweet_data)
            print(".", end="")
            sys.stdout.flush()
 
    return tweets_list
 
 
def get_tweets_data(username, soup):
    tweets_list = list()
    tweets_list.extend(get_this_page_tweets(soup))
 
def start(username = None):
    username = 'aagelfand'#get_username()
    url = "http://www.twitter.com/" + username
    print("\n\nDownloading tweets for " + username)
    response = None
    try:
        response = requests.get(url)
        
    except Exception as e:
        print(repr(e))
        sys.exit(1)
    
    if response.status_code != 200:
        print("Non success status code returned "+str(response.status_code))
        sys.exit(1)
 
    soup = BeautifulSoup(response.text, 'lxml')
 
    if soup.find("div", {"class": "errorpage-topbar"}):
        print("\n\n Error: Invalid username.")
        sys.exit(1)
 
    tweets = get_tweets_data(username, soup)
    return tweets
start()