#!/bin/bash

cd $(dirname ${0})
source .venv/bin/activate
python rss_feed_notifier/rss_feed_notifier.py