import bottle
import beaker.middleware
from bottle import route, redirect, post, run, request, hook
from instagram import client, subscriptions
from instagram.client import InstagramAPI

CONFIG = {
    'client_id': '923490f7659a44fb8a83db1a4134992f',
    'client_secret': '58999a8bbb0c42e78213585de310cafe',
    'redirect_uri': 'https://localhost'
}
unauthenticated_api = client.InstagramAPI(**CONFIG)


def access_token():
    scope = ('basic', 'public_content', 'follower_list', 'comments', 'relationships', 'likes')
    api = InstagramAPI(client_id=CONFIG['client_id'], client_secret=CONFIG['client_secret'],
                       redirect_uri=CONFIG['redirect_uri'])
    redirect_uri = api.get_authorize_login_url(scope=scope)

    print("Visit this page and authorize access in your browser:\n", redirect_uri)
    code = input("Paste in code in query string after redirect: ").strip()
    token1 = api.exchange_code_for_access_token(code)
    return token1


# token = access_token()
# print(type(token))
# print(token)
token = '3164739822.923490f.d687da010c1148c89aca2c42a5d02956'
api = InstagramAPI(client_id=CONFIG['client_id'], client_secret=CONFIG['client_secret'], access_token=token)
user = api.user('3164739822')
# user = api.user('1542518799')
print("Initialized user :" + user.username)
print("User Id :" + user.id)
print("User Full Name: " + user.full_name)
print("Number of Images Posted : " + str(user.counts['media']))
print("Number of Followers : " + str(user.counts['followed_by']))
print("Number Follows: " + str(user.counts['follows']))

users = api.user_search(q='oceantyy')
user2 = users[0]

print("Initialized user :" + user2.username)
print("User Id :" + user2.id)
print("User Full Name: " + user2.full_name)

# tag = api.tag_search(q='skate2work')
#
# tag_search, next_tag = api.tag_search(q="backclimateaction")
# tag_recent_media, next = api.tag_recent_media(tag_name=tag_search[0].name)
# photos = []
# for tag_media in tag_recent_media:
#     photos.append('<img src="%s"/>' % tag_media.get_standard_resolution_url())

print('end')
