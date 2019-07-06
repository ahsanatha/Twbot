import tweepy
import requests
from .firebase import *

# Application key
CONSUMER_KEY = 'YOUR-CONSUMER-KEY'
CONSUMER_SECRET = 'YOUR-CONSUMER-SECRET'


def get_api(request):
    # set up and return a twitter api object
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    access_key = request.session['access_key_tw']
    access_secret = request.session['access_secret_tw']
    oauth.set_access_token(access_key, access_secret)
    api = tweepy.API(oauth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    return api


def get_api_2(key, secret):
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    access_key = key
    access_secret = secret
    oauth.set_access_token(access_key, access_secret)
    api = tweepy.API(oauth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    return api


def delAllTweet_run(key, secret):
    statuses = []
    api = get_api_2(key, secret)
    try:
        me = api.me()
        user_id = str(me._json['id'])
        screen_name = me._json['screen_name']
        print('User id = ', user_id)
        context = get_from_fb(user_id)
    except tweepy.TweepError:
        print('Error, failed to get user id')
    try:
        statuses = api.user_timeline(user_id=user_id, screen_name=screen_name)
    except tweepy.TweepError:
        print('Error, failed to get user timeline')
    i = 0
    print('got ',len(statuses), ' statuses gonna remove it quickly')
    while len(statuses) != 0 and context['deleteAll']:
        temp = 0
        for status in statuses:
            api.destroy_status(status._json['id'])
            print('tweet id :', status._json['id'], 'destroyed!')
            i += 1
            temp += 1
        try:
            statuses = api.user_timeline(user_id)
        except tweepy.TweepError:
            print('Error, failed to get user timeline')
        data = {'numDeleted': context['numDeleted']+temp}
        push_to_fb(user_id,data)
        context = get_from_fb(user_id)
        print('==================== batch done ===================')
    print(i, ' tweets deleted')

