#!/usr/bin/env python

import tweepy

from .commandlineauth import check_setup, CommandlineException

CONSUMER_KEY    = "<Provided by Twitter>"
CONSUMER_SECRET = "<Provided by Twitter>"

# Get the values for these with request_authorisation()
ACCESS_KEY    = "<Manually entered by running this script with an empty value>"
ACCESS_SECRET = "<Manually entered by running this script with an empty value>"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)


# Methods --------------------------------------------------------------------

def fetch_random():

    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, api_root="/1.1")

    result = api.search("a", lang="en", count=50) # "a" == hack

    for tweet in strip_duplicates(result):

        if vet_tweet(api, tweet):
            print "Accepted: (%s) - %s" % (tweet.author.name.encode("utf_8"), tweet.text.encode("utf_8"))
            api.retweet(tweet.id)
            return True
        else:
            print "Rejected: (%s) - %s" % (tweet.author.name.encode("utf_8"), tweet.text.encode("utf_8"))


def vet_tweet(api, tweet):

    from re import match

    # Block anything with a link in it
    if "http" in tweet.text:
        return False

    if match(r"^(@|RT |I just entered to win |I just favorited ).*", tweet.text):
        return False

    if match(r".*(RT @|4sq\.com|gowal\.la|weight loss| SEO).*", tweet.text):
        return False

    if tweet.author.followers_count > 1000 or tweet.author.friends_count > 1000 or tweet.author.friends_count < 5:
        return False

    if match(r".*default_profile_.*", tweet.author.profile_image_url):
        return False

    return True


def strip_duplicates(tweets):

    r = []
    ids = []
    for tweet in tweets:
        if not tweet.id in ids:
            r.append(tweet)
        ids.append(tweet.id)

    return r


# Business Logic -------------------------------------------------------------

try:

    check_setup(auth, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    fetch_random()

except CommandlineException, e:

    print "  %s\n" % (e)

