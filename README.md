# rss-feed-notifier

A simple python script that reads a single feed and send pushover notifications to the configured account.

## Installation

1. git clone ! 
1. Create log folder.
1. (recommended) Create python environemnt in install requirements from requirements.txt
        pip install -r requirements.txt

## Usage

Create env file conf/rss-feed-notifier.yml
The file contents will look like this except filled in with your values.

        app_log_path: './log/rss-feed-notifier.log'
        url_log_path: './log/url_viewed.log'
        access_token: 'pushover app access token here'
        user_key: 'pushover user key here'

        - name: 'feed name'
            url: 'feed url'
            rule: 
              type: 'isNew'


## Build instructions

1. Install requirements for building
        - pip install pip -U
        - pip install setuptools -U
        - pip install wheel -U
1. python setup.py sdist bdist_wheel
1. Check the archive file in dist to make sure it contains the necessary files.
        tar tzf archive_filename.tgz
1. Check that description will render properly on PyPi
        twine check dist/*
1. Upload
        twine upload --repository-url https://test.pypi.org/legacy/ dist/*


## Useful Links

[List of Classifiers](https://pypi.python.org/pypi?%253Aaction=list_classifiers)
[Pushover API Documentation](https://pushover.net/api)


