# -*- coding: utf-8 -*-

#
# This is just a helper library I wrote to make it easy to write command-line
# scripts that talk to Twitter via tweepy.  It handles the initial stages of
# creating auth keys from consumer keys, and makes the assumption that you're
# writing to a single feed.
#

class CommandlineException(Exception):

    def __init__(self, message):
        self._set_message(message)


    def __unicode__(self):
        return self._get_message()


    def __str__(self):
        return self.__unicode__()


    def _get_message(self):
        return self._message


    def _set_message(self, message):
        self._message = message


    message = property(_get_message, _set_message)



def request_authorisation(auth):
    """
        Runs only if ACCESS_KEY or ACCESS_SECRET aren't already set, we use
        this to help configure the script to authenticate against Twitter.
    """

    auth_url = auth.get_authorization_url()

    print 'Please authorize: ' + auth_url

    verifier = raw_input('PIN: ').strip()
    auth.get_access_token(verifier)

    print "Put these at the top of this script"
    print "ACCESS_KEY    = '%s'" % auth.access_token.key
    print "ACCESS_SECRET = '%s'" % auth.access_token.secret



def check_setup(auth, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):

    if not CONSUMER_KEY or not CONSUMER_SECRET:

        print "\n  You must specify a CONSUMER_KEY and CONSUMER_SECRET in this script for it to work\n"

    else:

        if not ACCESS_KEY or not ACCESS_SECRET:

            from commandlineauth import request_authorisation

            request_authorisation(auth)

        else:

            return True

    raise CommandlineException("Exiting prematurely due to configuration errors")

