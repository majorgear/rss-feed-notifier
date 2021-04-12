import feedparser
import os
import http.client, urllib
import logging
import time
import yaml
import re
import argparse
# class Feed(object):

def create_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument( "--config", default="conf/rss-feed-notifier.yml", help="Path to yml configuration file."  )
    # parser.add_argument( "-c,--config", actions="store", help="Path to yml configuration file."  )
    args = parser.parse_args()
    print(args.config)
    return args 

def contains(words,content):
    for word in words:
        if re.search(r"\b" + re.escape(word) + r"\b", content):
            return True
    return False

# def is_satisfied( rule )
#     if rule['type'] == 'contains'
#         return contains( rule['words'] )
#     else:
#         logger.error( f"Unknown rule type {rule['type']}" )
#         return False

def load_config( file_path):
    with open( file_path, 'r') as f:
        try:
            return yaml.load(f, Loader=yaml.FullLoader)
        except:
            raise Exception

def send_pushover_msg(title, msg, priority, user_key, access_token):
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

# def contains_wanted(in_str):
#     # returns true if the in_str contains a keyword
#     # we are interested in. Case-insensitive
#     for wrd in key_words:
#         if wrd.lower() in in_str:
#             return True
#     return False

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
    args = create_arguments()
    config = load_config(args.config)
    app_log_path = config['app_log_path']
    access_token = config['access_token']
    user_key = config['user_key']
    rss_feeds = config['rss_feeds']
    url_log_path = config['url_log_path']

    for rss_feed in rss_feeds:
        # rss = 'https://www.reddit.com/r/Python/.rss'
        if not rss_feed['enabled']:
            pass
        else:
            feed = feedparser.parse(rss_feed['url'])
            for key in feed["entries"]: 
                url = key['links'][0]['href']
                title = key['title']
                content = key['content']

                if url_is_new(url,url_log_path):
                    if 'rule' not in rss_feed.keys():
                        # create message body
                        print(f"{title} - {url}")
                        msgtitle = title
                        msg = f"{title}\n{url}"
                        priority = -1  if not 'priority' in rss_feed.keys() else rss_feed['priority']   
                        send_pushover_msg(msgtitle, msg, priority, user_key, access_token)
                    elif 'contains' in rss_feed['rule']['type'] and contains( rss_feed['rule']['words'], content[0]['value'] ):
                        # create message body
                        print(f"{title} - {url}")
                        msgtitle = title
                        msg = f"{title}\n{url}"
                        priority = -1  if not 'priority' in rss_feed.keys() else rss_feed['priority']   
                        send_pushover_msg(msgtitle, msg, priority, user_key, access_token)

                    with open( url_log_path, 'a') as f:
                        f.write('{}\n'.format(url))


if __name__ == "__main__":
    main()

