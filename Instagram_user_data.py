import concurrent.futures
import json
import requests
import warnings
import csv
import re

name = 'yy_god'
url = 'http://instagram.com/' + name
resp = requests.get(url)
position = re.search('window._sharedData', resp.text).span()
tmp1 = resp.text[int(position[1] + 3):]
position2 = re.search('</script>', tmp1).span()
tmp2 = tmp1[:position2[0] - 1]
data = json.loads(tmp2)
print(data)
print(data['language_code'])
print(data['entry_data']['ProfilePage'][0]['user'])
