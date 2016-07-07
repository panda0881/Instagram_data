import json
import requests
import re

name = 'boostedboard'
resp = requests.get('http://instagram.com/explore/tags/' + name)
tmp1 = resp.text[int(re.search('window._sharedData', resp.text).span()[1] + 3):]
tmp2 = tmp1[:re.search('</script>', tmp1).span()[0] - 1]
data = json.loads(tmp2)
tag = data['entry_data']['TagPage'][0]['tag']
print('top_posts: ')
for media in tag['top_posts']['nodes']:
    resp = requests.get('http://instagram.com/p/' + media['code'])
    tmp1 = resp.text[int(re.search('window._sharedData', resp.text).span()[1] + 3):]
    tmp2 = tmp1[:re.search('</script>', tmp1).span()[0] - 1]
    top_posts_data = json.loads(tmp2)
    print('username: ' + top_posts_data['entry_data']['PostPage'][0]['media']['owner']['username'])
print('media: ')
for media in tag['media']['nodes']:
    resp = requests.get('http://instagram.com/p/' + media['code'])
    tmp1 = resp.text[int(re.search('window._sharedData', resp.text).span()[1] + 3):]
    tmp2 = tmp1[:re.search('</script>', tmp1).span()[0] - 1]
    media_data = json.loads(tmp2)
    print('username: ' + media_data['entry_data']['PostPage'][0]['media']['owner']['username'])
print('finish...')
