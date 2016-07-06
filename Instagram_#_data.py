import concurrent.futures
import json
import requests
import warnings
import csv
import re

name = 'boostedboard'
resp = requests.get('http://instagram.com/explore/tags/' + name)
tmp1 = resp.text[int(re.search('window._sharedData', resp.text).span()[1] + 3):]
tmp2 = tmp1[:re.search('</script>', tmp1).span()[0] - 1]
data = json.loads(tmp2)

tag = data['entry_data']['TagPage'][0]['tag']

print('top_posts: ')
for media in tag['top_posts']['nodes']:
    url = 'http://instagram.com/p/' + media['code']
    resp = requests.get(url)
    position = re.search('window._sharedData', resp.text).span()
    tmp1 = resp.text[int(position[1] + 3):]
    position2 = re.search('</script>', tmp1).span()
    tmp2 = tmp1[:position2[0] - 1]
    data_testing = json.loads(tmp2)
    print('username: ' + data_testing['entry_data']['PostPage'][0]['media']['owner']['username'])


print('media: ')
for media in tag['media']['nodes']:
    url = 'http://instagram.com/p/' + media['code']
    resp = requests.get(url)
    position = re.search('window._sharedData', resp.text).span()
    tmp1 = resp.text[int(position[1] + 3):]
    position2 = re.search('</script>', tmp1).span()
    tmp2 = tmp1[:position2[0] - 1]
    data_testing = json.loads(tmp2)
    print('username: ' + data_testing['entry_data']['PostPage'][0]['media']['owner']['username'])

print('finish...')


