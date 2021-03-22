#!/bin/bash

cd $(dirname ${0})
source .venv/bin/activate
python rss-feed-notifier/rss-feed-notifier.py