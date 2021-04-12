import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="rss-feed-notifier",
    version="0.1.0",
    description="A simple python script that reads a single feed and send pushover notifications to the configured account.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/majorgear/rss-feed-notifier",
    author="John Gooch",
    author_email="majorgear@majorgear.tech",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["feedparser", "PyYAML" ],
   entry_points={
       "console_scripts": [
           "majorgear=rss_feed_notifier.__main__:main"
       ]
   },
)
