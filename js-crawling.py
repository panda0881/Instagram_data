import requests
from Instagram_Spider import *

follower_list = list()
s = requests.session()
cookie = 'mid=VyoH4QAEAAHSM1L-WuJx0TEnosOT; fbm_124024574287414=base_domain=.instagram.com; ' \
         'sessionid=IGSC180da69381c0a14e9dc9f9e4bc769c4019e8f3583dcd817d5bc7968985b55952%3Anv7S014E4DnNKVqcm8aj7S' \
         'pMQeJEFoGM%3A%7B%22_token_ver%22%3A2%2C%22_auth_user_id%22%3A3164739822%2C%22_token%22%3A%223164739822%' \
         '3AfEsxWL60kGe9CTcT6SZip5YZ5FkYrdGL%3A0343dc6e70184bce7f5dcad622b15ea4c9f9db7527ff9183d1b8415e16a66c62%2' \
         '2%2C%22asns%22%3A%7B%2261.216.163.33%22%3A3462%2C%22time%22%3A1468545499%7D%2C%22_auth_user_backend%22%' \
         '3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22last_refreshed%22%3A1468545499.109788%2C%22_' \
         'platform%22%3A4%7D; ig_pr=1; ig_vw=729; fbsr_124024574287414=7NY3P64retR7WLLnDGB-12lgJNuu4T8sMZfjnQjqvo' \
         '4.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUFDTnl1aUhpWUdjOHVJWFFCbXF0dFdaLUc5SngtcklqaGNpalhNb' \
         'DFpQ0hhZDZyM3ZrNHRkWDUzYWhtdmxZZ1dwTGRLbXo2a1lnLW9XS3J0OWlZcUVvUEFubngyTnlrenBoUGJrX09wamdQWVQ1WExVX1lO' \
         'RExvWEMxdzdYZFVUbWpzb3UxVW45LXBLLWxlaUotN3FfVDdXdHRUc1FhT3JmYXRVYmszWHpfY1laZUl4RXcwRUlLWERJRTBoTEtSaUY' \
         '5Z29aWkM4M3BvblZwQWgyY1BjTUgxR2RrQlBkSEEzOUJIbVFQMjBXWnJwa2ZfRy1kMVZrY1FyUlk3a1ozQTQza2lGbEtCeUtpY0tmX2' \
         '9aRlBLWVpZNms1MUl4WTlrZEpjbFpZYVk0OWFybWhvbTJOaWZRTldyc2V3T3lzUGkxOUVOQVZTY1poR0NfU3hEa2xmR0JjMCIsImlzc' \
         '3VlZF9hdCI6MTQ2ODU4NzI4NSwidXNlcl9pZCI6IjEwMDAwNDI2NTg2MDQ3MCJ9; s_network=; csrftoken=7807d567fcdc9d26' \
         'b384856155415008; ds_user_id=' + str(3164739822)



def get_user_follower_list(name, id, end_cursor=None):
    # spider = InstagramSpider()
    # username = 'hongming0611'
    # password = input('hi, ' + username + 'please give me your password: ')
    # spider.login(username, password)
    referer = 'https://www.instagram.com/' + name + '/'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'origin': 'https://www.instagram.com',
        'referer': referer,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/51.0.2704.103 Safari/537.36',
        'x-csrftoken': '7807d567fcdc9d26b384856155415008',
        'x-instagram-ajax': 1,
        'x-requested-with': 'XMLHttpRequest'
    }
    if not end_cursor:
        data = 'q=ig_user(' + str(id) +')+%7B%0A++followed_by.first(10)+%7B%0A++++count%2C%0A++++page_info+%7B%0A++++++end_cursor%2C%0A++++++has_next_page%0A++++%7D%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++is_verified%2C%0A++++++followed_by_viewer%2C%0A++++++requested_by_viewer%2C%0A++++++full_name%2C%0A++++++profile_pic_url%2C%0A++++++username%0A++++%7D%0A++%7D%0A%7D%0A&ref=relationships%3A%3Afollow_list'
        result = s.post('https://www.instagram.com/query/', data=data, headers=headers)
        data = result.json()
        for user in data['followed_by']['nodes']:
            follower_list.append(user['username'])
        next_page = data['followed_by']['page_info']['has_next_page']
        next_end_cursor = data['followed_by']['page_info']['end_cursor']
    else:
        data = 'q=ig_user(' + str(id) +')+%7B%0A++followed_by.after(' + end_cursor + ', 10)+%7B%0A++++count%2C%0A++++page_info+%7B%0A++++++end_cursor%2C%0A++++++has_next_page%0A++++%7D%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++is_verified%2C%0A++++++followed_by_viewer%2C%0A++++++requested_by_viewer%2C%0A++++++full_name%2C%0A++++++profile_pic_url%2C%0A++++++username%0A++++%7D%0A++%7D%0A%7D%0A&ref=relationships%3A%3Afollow_list'
        result = s.post('https://www.instagram.com/query/', data=data, headers=headers)
        data = result.json()
        for user in data['followed_by']['nodes']:
            follower_list.append(user['username'])
        next_page = data['followed_by']['page_info']['has_next_page']
        next_end_cursor = data['followed_by']['page_info']['end_cursor']
    if next_page:
        get_user_follower_list(name, id, next_end_cursor)



get_user_follower_list('yy_god', 1542518799)


print('end')
