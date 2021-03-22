# rss-feed-notifier

A simple python script that reads a single feed and send pushover notifications to the configured account.

## Installation

1. git clone ! 
1. Create log folder.
1. (recommended) Create python environemnt in install requirements from requirements.txt
        pip install -r requirements.txt

## Usage

Create env file ./rss-feed-notifier.env
The file contents will look like this except filled in with your values.

    RSS='rss feed url here'
    ACCESS_TOKEN='pushover app access token here'
    USER_KEY="pushover user key here"
