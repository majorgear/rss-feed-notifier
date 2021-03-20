import feedparser
import pprint
# from pushbullet import Pushbullet
from dotenv import load_dotenv
import os
import http.client, urllib
import logging
import time

app_log_path = "./log/rss-feed-notifier.log"
url_log_path = "./log/url_viewed.log"

def send_pushover_msg(title, msg, user_key, access_token):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": access_token,
        "user": user_key,
        "message": msg,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    time.sleep(1)


# Just some sample keywords to search for in the title
key_words = ['Flask','Pyramid', 'JOB']


def contains_wanted(in_str):
    # returns true if the in_str contains a keyword
    # we are interested in. Case-insensitive
    for wrd in key_words:
        if wrd.lower() in in_str:
            return True
    return False

def url_is_new(urlstr):
    # returns true if the url string does not exist 
    # in the list of strings extracted from the text file
    # get the urls we have seen prior
    if not os.path.exists("log/views_urls.log"):
        return True
    else:
        with open( url_log_path, 'r') as f:
            urls = f.readlines()
            urls = [url.rstrip() for url in urls] # remove the '\n' char
        if urlstr in urls:
            return False
        else:
            return True

def main():

    # args = create_arguments()
    # conf = load_config()
    load_dotenv(dotenv_path='./rss-feed-notifier.env')
    access_token = os.getenv("ACCESS_TOKEN")
    user_key = os.getenv("USER_KEY")
    rss = os.getenv("RSS")
    # rss = 'https://www.reddit.com/r/Python/.rss'
    feed = feedparser.parse(rss)
    for key in feed["entries"]: 
        url = key['links'][0]['href']
        title = key['title']
        content = key['content']

        # if contains_wanted(title.lower()) and url_is_new(url):
        if url_is_new(url):
            print(f"{title} - {url}")

            msgtitle = title
            msg = f"{title}\n{url}"

            send_pushover_msg(msgtitle, msg, user_key, access_token)

            with open( url_log_path, 'a') as f:
                f.write('{}\n'.format(url))

if __name__ == "__main__":
    main()

