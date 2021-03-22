import feedparser
import pprint
from dotenv import load_dotenv
import os
import http.client, urllib
import logging
import time
import yaml

# class Feed(object):

def load_config( file_path):
    with open( file_path, 'r') as f:
        try:
            return yaml.load(f, Loader=yaml.FullLoader)
        except:
            raise Exception

def send_pushover_msg(title, msg, user_key, access_token):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": access_token,
        "user": user_key,
        "title": title,
        "message": msg,
        "priority": 1,
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

def url_is_new(urlstr, url_log_path):
    # returns true if the url string does not exist 
    # in the list of strings extracted from the text file
    # get the urls we have seen prior
    if not os.path.exists(url_log_path):
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
    config = load_config('./conf/rss-feed-notifier.yml')
    app_log_path = config['app_log_path']
    access_token = config['access_token']
    user_key = config['user_key']
    rss_feeds = config['rss_feeds']
    url_log_path = config['url_log_path']


    for rss_feed in rss_feeds:
        # rss = 'https://www.reddit.com/r/Python/.rss'
        feed = feedparser.parse(rss_feed['url'])
        for key in feed["entries"]: 
            url = key['links'][0]['href']
            title = key['title']
            content = key['content']

            # if contains_wanted(title.lower()) and url_is_new(url):
            if url_is_new(url,url_log_path):
                # create message body
                print(f"{title} - {url}")
                msgtitle = title
                msg = f"{title}\n{url}"
                priority = 0
                send_pushover_msg(msgtitle, msg, priority, user_key, access_token)

                with open( url_log_path, 'a') as f:
                    f.write('{}\n'.format(url))

if __name__ == "__main__":
    main()

