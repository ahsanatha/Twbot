from django.shortcuts import *
from .utils import *
from .firebase import *
from rq import Queue
from worker import conn

q = Queue(connection=conn)
context = {
    "deleteAll": False,
    "numDeleted": 0,
}

def index(request):
    return render_to_response('twitter_auth/index.html')

def logout(request):
    request.session['logged'] = False
    request.session.delete('request_token')
    request.session.delete('access_key_tw')
    request.session.delete('access_secret_tw')
    return redirect('index')

def auth(request):
    print(CONSUMER_SECRET,CONSUMER_KEY)
    oauth = tweepy.OAuthHandler(
        CONSUMER_KEY, CONSUMER_SECRET,)  
    auth_url = oauth.get_authorization_url(True)
    response = redirect(auth_url)
    request.session['request_token'] = oauth.request_token
    return response

def callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(
        CONSUMER_KEY, CONSUMER_SECRET,)
    token = request.session.get('request_token')
    request.session.delete('request_token')
    oauth.request_token = token
    # get the access token and store
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error, failed to get access token')

    request.session['access_key_tw'] = oauth.access_token
    request.session['access_secret_tw'] = oauth.access_token_secret
    request.session['logged'] = True
    response = redirect('home')
    return response

def update_context(request):
    global context
    api = get_api(request)
    context['user'] = api.me()
    request.session['user_id'] = context['user']._json['id']
    result = get_from_fb(str(request.session.get('user_id')))
    context['deleteAll'] = result['deleteAll']
    context['numDeleted'] = result['numDeleted']

def home(request):
    global context
    # print(context['user']._json['id'])
    update_context(request)
    if not(request.session.get('logged')):
        return redirect('index')
    return render(request, 'twitter_auth/home.html', context)


def delAllTweet(request):
    global context
    if not(request.session.get('logged')):
        return redirect('index')
    # update_context(request)
    if (request.GET.get('delState')):
        delete(request.GET.get('delState'), 'all', request)
    update_context(request)
    return render(request, 'twitter_auth/delAllTw.html', context)


def delete(status, type, request):
    global q
    if (type == 'all'):
        if(status == 'Delete'):
            push_to_fb(str(request.session['user_id']),{"deleteAll":True})
            q.enqueue(
                delAllTweet_run, request.session['access_key_tw'], request.session['access_secret_tw'])
        elif (status == 'Stop'):
            push_to_fb(str(request.session['user_id']),{"deleteAll":False})