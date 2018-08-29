# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 21:35:36 2018

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
 
 
def get_username():
    # if username is not passed
    if len(sys.argv) < 2:
        usage()
    username = sys.argv[1].strip().lower()
    if not username:
        usage()
 
    return username
 
 
def start(username = None):
    username = get_username()
    url = "http://www.twitter.com/" + username
    print("\n\nDownloading tweets for " + username)
    response = None
    try:
        response = requests.get(url)
        
        
        with open("A.lxml", "wb") as f:
            f.write(response.content)
        # read it back in
        with open("A.lxml") as f:
          soup = BeautifulSoup(f)
        
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