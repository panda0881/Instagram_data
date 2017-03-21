import concurrent.futures
import json
import requests
import re
import os
from collections import Counter
import time


class InstagramSpider:
    def __init__(self):
        self.numPosts = 0
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self.future_to_item = {}
        self.s = requests.session()
        self.full_media_list = list()
        self.follower_list = list()
        self.follow_list = list()
        self.username = ''
        self.password = ''
        self.owner_id = 0

    @staticmethod
    def list_formatting(input_list):
        list1 = Counter(input_list).most_common()
        output_list = list()
        for pair in list1:
            if pair[1] <= 1:
                break
            output_list.append(pair)
        return output_list

    def login(self, username, password):
        self.username = username
        self.password = password
        owner_data = self.get_user_data(username)
        self.owner_id = owner_data['id']
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
            'content-length': '23',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'mid=V39AvQAEAAEIwy8g1C7EViIlodxd; s_network=; ig_pr=1; ig_vw=650; '
                      'csrftoken=3r8AwU3xWRhQMFIMz5b6ICn6Pfa4A5ZV',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/login/',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/51.0.2704.103 Safari/537.36',
            'x-csrftoken': '3r8AwU3xWRhQMFIMz5b6ICn6Pfa4A5ZV',
            'x-instagram-ajax': '1',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {'username': username, 'password': password}
        self.s.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=headers)

    def get_user_data(self, name):
        resp = self.s.get('http://instagram.com/' + name)
        tmp1 = resp.text[int(re.search('window._sharedData', resp.text).span()[1] + 3):]
        tmp2 = tmp1[:re.search('</script>', tmp1).span()[0] - 1]
        data = json.loads(tmp2)['entry_data']['ProfilePage'][0]['user']
        return data

    def get_tag_data(self, tag_name):
        resp = self.s.get('http://instagram.com/explore/tags/' + tag_name)
        tmp1 = resp.text[int(re.search('window._sharedData', resp.text).span()[1] + 3):]
        tmp2 = tmp1[:re.search('</script>', tmp1).span()[0] - 1]
        data = json.loads(tmp2)['entry_data']['TagPage'][0]['tag']
        return data

    def get_media_data(self, media_code):
        resp = self.s.get('http://instagram.com/p/' + media_code)
        tmp1 = resp.text[int(re.search('window._sharedData', resp.text).span()[1] + 3):]
        tmp2 = tmp1[:re.search('</script>', tmp1).span()[0] - 1]
        data = json.loads(tmp2)['entry_data']['PostPage'][0]['media']
        return data

    def get_user_full_media_data(self, name, max_id=None):
        url = 'http://instagram.com/' + name + '/media'
        if max_id:
            url += '?&max_id=' + max_id
        resp = requests.get(url)
        try:
            media = json.loads(resp.text)
        except:
            print('there is something wrong with this user')
            return
        self.numPosts += len(media['items'])
        print('collecting data from ' + str(self.numPosts) + 'medias')
        for item in media['items']:
            self.full_media_list.append(item['code'])
        if 'more_available' in media and media['more_available'] is True:
            max_id = media['items'][-1]['id']
            self.get_user_full_media_data(name=name, max_id=max_id)

    def collect_followers(self, cookie, name, user_id, end_cursor=None):
        print('Current follower list number: ' + str(len(self.follower_list)))
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
            data = 'q=ig_user(' + user_id + \
                   ')+%7B%0A++followed_by.first(10)+%7B%0A++++count%2C%0A++++page_info+%7B%0A++++++end_cursor%2C%0A+' \
                   '+++++has_next_page%0A++++%7D%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++is_verified%2C%0A++++++fol' \
                   'lowed_by_viewer%2C%0A++++++requested_by_viewer%2C%0A++++++full_name%2C%0A++++++profile_pic_url%2' \
                   'C%0A++++++username%0A++++%7D%0A++%7D%0A%7D%0A&ref=relationships%3A%3Afollow_list'
            result = self.s.post('https://www.instagram.com/query/', data=data, headers=headers)
            data = result.json()
            for user in data['followed_by']['nodes']:
                self.follower_list.append(user['username'])
            next_page = data['followed_by']['page_info']['has_next_page']
            next_end_cursor = data['followed_by']['page_info']['end_cursor']
        else:
            data = 'q=ig_user(' + user_id + ')+%7B%0A++followed_by.after(' + end_cursor + \
                   ', 10)+%7B%0A++++count%2C%0A++++page_info+%7B%0A++++++end_cursor%2C%0A++++++has_next_page%0A++++%' \
                   '7D%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++is_verified%2C%0A++++++followed_by_viewer%2C%0A+++++' \
                   '+requested_by_viewer%2C%0A++++++full_name%2C%0A++++++profile_pic_url%2C%0A++++++username%0A++++%' \
                   '7D%0A++%7D%0A%7D%0A&ref=relationships%3A%3Afollow_list'
            result = self.s.post('https://www.instagram.com/query/', data=data, headers=headers)
            data = result.json()
            for user in data['followed_by']['nodes']:
                self.follower_list.append(user['username'])
            next_page = data['followed_by']['page_info']['has_next_page']
            next_end_cursor = data['followed_by']['page_info']['end_cursor']
        if next_page:
            self.collect_followers(cookie, name, user_id, next_end_cursor)

    def collect_follows(self, cookie, name, user_id, end_cursor=None):
        print('Current follow list number: ' + str(len(self.follow_list)))
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
            data = 'q=ig_user(' + user_id + \
                   ')+%7B%0A++follows.first(10)+%7B%0A++++count%2C%0A++++page_info+%7B%0A++++++end_cursor%2C%0A+++++' \
                   '+has_next_page%0A++++%7D%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++is_verified%2C%0A++++++followe' \
                   'd_by_viewer%2C%0A++++++requested_by_viewer%2C%0A++++++full_name%2C%0A++++++profile_pic_url%2C%0A' \
                   '++++++username%0A++++%7D%0A++%7D%0A%7D%0A&ref=relationships%3A%3Afollow_list'
            result = self.s.post('https://www.instagram.com/query/', data=data, headers=headers)
            data = result.json()
            for user in data['follows']['nodes']:
                self.follow_list.append(user['username'])
            next_page = data['follows']['page_info']['has_next_page']
            next_end_cursor = data['follows']['page_info']['end_cursor']
        else:
            data = 'q=ig_user(' + user_id + ')+%7B%0A++follows.after(' + end_cursor + \
                   ', 10)+%7B%0A++++count%2C%0A++++page_info+%7B%0A++++++end_cursor%2C%0A++++++has_next_page%0A++++%' \
                   '7D%2C%0A++++nodes+%7B%0A++++++id%2C%0A++++++is_verified%2C%0A++++++followed_by_viewer%2C%0A+++++' \
                   '+requested_by_viewer%2C%0A++++++full_name%2C%0A++++++profile_pic_url%2C%0A++++++username%0A++++%' \
                   '7D%0A++%7D%0A%7D%0A&ref=relationships%3A%3Afollow_list'
            result = self.s.post('https://www.instagram.com/query/', data=data, headers=headers)
            data = result.json()
            for user in data['follows']['nodes']:
                self.follow_list.append(user['username'])
            next_page = data['follows']['page_info']['has_next_page']
            next_end_cursor = data['follows']['page_info']['end_cursor']
        if next_page:
            self.collect_follows(cookie, name, user_id, next_end_cursor)

    def get_user_followers_and_follows(self, name):
        self.follower_list = list()
        self.follow_list = list()
        cookie = 'mid=VyoH4QAEAAHSM1L-WuJx0TEnosOT; fbm_124024574287414=base_domain=.instagram.com; sessionid=IGSC94' \
                 '18aaf857177c99ed52a2e6c37e6a251074f891282a715fdd7c3aca86705f08%3Aw2geyFDrzzVKRERueIyLgESNUXoOcAqE%' \
                 '3A%7B%22_token_ver%22%3A2%2C%22_auth_user_id%22%3A3164739822%2C%22_token%22%3A%223164739822%3AfEsx' \
                 'WL60kGe9CTcT6SZip5YZ5FkYrdGL%3A0343dc6e70184bce7f5dcad622b15ea4c9f9db7527ff9183d1b8415e16a66c62%22' \
                 '%2C%22asns%22%3A%7B%2261.216.161.9%22%3A3462%2C%22time%22%3A1468633377%7D%2C%22_auth_user_backend%' \
                 '22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22last_refreshed%22%3A1468633378.08871' \
                 '9%2C%22_platform%22%3A4%7D; s_network=; ig_pr=1; ig_vw=729; fbsr_124024574287414=NB0xYjmjejvWC_OH0' \
                 '3uAQgqjPuT6piawnl6bht1Eue4.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUFfNDlJbGprRTBUZ2JPSXZ' \
                 'PQ0FpVEFpek5RMFRoM0x2TTNLOTFnRGVXVlhiaXNRSFdnSjRrOWQ3OFJRaGd1RmFGeWROQy1kU0pibmpTTmJFWjZISVU5bnd1a' \
                 'HczVTdVMF9XNGZOekVxWnNpT2IwT1dVcVdLeWJKYUVrRFRSRzhfRUZlUmtxejdsOWVReFBGTm9qNWtGQ0E0ODc3Wl9YMmg0RER' \
                 '3SFdUdkxQSmhGdlpEejA5ME45YXZsOGw0eFJ4VzBvcVpwRG4yQW45dXlnMU4yOTFDcjNMTU5FT3pXb0l1RW02UHRJeEdJU0xHU' \
                 'VgtME40c09vdDRzekxHY0lvTjhaREpkRVNFc2szMU5RZHoyOEJxVGNZTExMZTBjbE1rbDJVcWNhOGNsTFFvTUFHdGw2OU5sVk5' \
                 'rZGp1dTdHUTl2cHIzaTU4cWkwalJBelRLNnI4ZFktSSIsImlzc3VlZF9hdCI6MTQ2ODY1ODk4OSwidXNlcl9pZCI6IjEwMDAwN' \
                 'DI2NTg2MDQ3MCJ9; csrftoken=7807d567fcdc9d26b384856155415008; ds_user_id=' + str(self.owner_id)
        data = self.get_user_data(name)
        user_id = data['id']
        self.collect_followers(cookie, name, user_id)
        self.collect_follows(cookie, name, user_id)
        return self.follower_list, self.follow_list

    def download_user_media(self, name, max_id=None):
        url = 'http://instagram.com/' + name + '/media'
        if max_id:
            url += '?&max_id=' + max_id
        resp = requests.get(url)
        media = json.loads(resp.text)
        self.numPosts += len(media['items'])

        for item in media['items']:
            future = self.executor.submit(self.download, item, './' + name)
            self.future_to_item[future] = item

        if 'more_available' in media and media['more_available'] is True:
            max_id = media['items'][-1]['id']
            self.download_user_media(name=name, max_id=max_id)

    @staticmethod
    def download(item, save_dir='./'):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        item['url'] = item[item['type'] + 's']['standard_resolution']['url']
        item['url'] = re.sub(r'/s\d{3,}x\d{3,}/', '/', item['url'])
        base_name = item['url'].split('/')[-1].split('?')[0]
        file_path = os.path.join(save_dir, base_name)
        with open(file_path, 'wb') as file:
            file.write(requests.get(item['url']).content)
        file_time = int(item['created_time'])
        os.utime(file_path, (file_time, file_time))

    def get_comment_from_media(self, media_code):
        data = self.get_media_data(media_code)
        username = data['owner']['username']
        comment_list = list()
        for comment in data['comments']['nodes']:
            if comment['user']['username'] == username:
                comment_list.append(comment['text'])
                print(comment['text'])
        return comment_list

    def get_tag_from_media(self, media_code):
        data = self.get_media_data(media_code)
        tag_list = list()
        sentences = list()
        if 'caption' in data.keys():
            sentences.append(data['caption'])
        for comment in data['comments']['nodes']:
            if data['owner']['username'] == comment['user']['username']:
                sentences.append(comment['text'])
        for sentence in sentences:
            number = sentence.count('#')
            position = sentence.find('#')
            if number > 0:
                while position >= 0:
                    string = sentence[position + 1:]
                    pos1 = string.find(' ')
                    pos2 = string.find('\n')
                    pos3 = string.find('#')
                    l = [pos1, pos2, pos3, 0]
                    l.sort()
                    if l.index(0) < 3:
                        pos = l[l.index(0) + 1]
                        tag = string[:pos]
                        tag_list.append(tag)
                        sentence = string[pos:]
                        position = sentence.find('#')
                    else:
                        tag = string
                        tag_list.append(tag)
                        sentence = ''
                        position = sentence.find('#')
        tag_list = list(set(tag_list))
        return tag_list

    def collect_media_list(self, tag_name, end_cursor):
        # You may need to change the time of delay based on your own network situation and need.
        time.sleep(0.5)
        cookie = 'mid=VyoH4QAEAAHSM1L-WuJx0TEnosOT; fbm_124024574287414=base_domain=.instagram.com; sessionid=IGSC94' \
                 '18aaf857177c99ed52a2e6c37e6a251074f891282a715fdd7c3aca86705f08%3Aw2geyFDrzzVKRERueIyLgESNUXoOcAqE%' \
                 '3A%7B%22_token_ver%22%3A2%2C%22_auth_user_id%22%3A3164739822%2C%22_token%22%3A%223164739822%3AfEsx' \
                 'WL60kGe9CTcT6SZip5YZ5FkYrdGL%3A0343dc6e70184bce7f5dcad622b15ea4c9f9db7527ff9183d1b8415e16a66c62%22' \
                 '%2C%22asns%22%3A%7B%2261.216.161.9%22%3A3462%2C%22time%22%3A1468633377%7D%2C%22_auth_user_backend%' \
                 '22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22last_refreshed%22%3A1468633378.08871' \
                 '9%2C%22_platform%22%3A4%7D; ig_pr=1; ig_vw=729; csrftoken=7807d567fcdc9d26b384856155415008; s_netw' \
                 'ork=; ds_user_id=' + str(self.owner_id)
        referer = 'https://www.instagram.com/explore/tags/' + tag_name + '/'
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
        data = 'q=ig_hashtag(' + tag_name + ')+%7B+media.after(' + end_cursor + \
               '%2C+10)+%7B%0A++count%2C%0A++nodes+%7B%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++coun' \
               't%0A++++%7D%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++' \
               'display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%' \
               '7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A' \
               '+%7D&ref=tags%3A%3Ashow'
        tmp_result = self.s.post('https://www.instagram.com/query/', data=data, headers=headers)
        result = tmp_result.json()
        try:
            for media in result['media']['nodes']:
                self.full_media_list.append(media['code'])
            print('has collected: ' + str(len(self.full_media_list)) + 'medias')
        except KeyError:
            print('There is something wrong with this hashtag...')
            return
        if result['media']['page_info']['has_next_page']:
            self.collect_media_list(tag_name, result['media']['page_info']['end_cursor'])
        else:
            return

    def get_media_from_tag(self, tag_name):
        top_posts_media_list = list()
        self.full_media_list = list()
        data = self.get_tag_data(tag_name)
        for media in data['top_posts']['nodes']:
            top_posts_media_list.append(media['code'])
        for media in data['media']['nodes']:
            self.full_media_list.append(media['code'])
        if data['media']['page_info']['has_next_page']:
            self.collect_media_list(tag_name, data['media']['page_info']['end_cursor'])
            print('finish collecting media')
        return top_posts_media_list, self.full_media_list

    def get_user_from_media(self, media_code):
        data = self.get_media_data(media_code)
        user_list = list()
        user_list.append(data['owner']['username'])
        # for comment in data['comments']['nodes']:
        #     user_list.append(comment['user']['username'])
        # for like in data['likes']['nodes']:
        #     user_list.append(like['user']['username'])
        user_list = list(set(user_list))
        return user_list

    @staticmethod
    def get_media_from_user(name):
        url = 'http://instagram.com/' + name + '/media'
        resp = requests.get(url)
        media = json.loads(resp.text)
        media_list = list()
        for item in media['items']:
            media_list.append(item['code'])
        return media_list

    def get_user_from_tag(self, tag_name):
        top_medias, medias = self.get_media_from_tag(tag_name)
        user_list = list()
        current_number = 0
        for media in medias:
            current_number += 1
            print('getting information for: ' + media + '(' + str(current_number) + '/' + str(len(medias)) + ')')
            tmp = self.get_user_from_media(media)
            for user in tmp:
                user_list.append(user)
        user_list = list(set(user_list))
        final_user_list = list()
        print('total potential user: ' + str(len(user_list)))
        current_number = 0
        for user in user_list:
            current_number += 1
            print('Verifying ' + user + '(' + str(current_number) + '/' + str(len(user_list)) + ')')
            data = self.get_user_data(user)
            if data['is_private'] == False and data['followed_by']['count'] > 500:
                final_user_list.append(user)
        return final_user_list

    def get_tag_from_user(self, name):
        media_list = self.get_media_from_user(name)
        tag_list = list()
        print('total number of medias from this user: ' + str(len(media_list)))
        for media in media_list:
            print('getting tag from media: ' + media)
            tmp = self.get_tag_from_media(media)
            for tag in tmp:
                tag_list.append(tag)
        tag_list = self.list_formatting(tag_list)
        return tag_list

    def get_all_tag_from_user(self, name):
        self.full_media_list = list()
        self.numPosts = 0
        self.get_user_full_media_data(name)
        tag_list = list()
        print('getting data for user: ' + name)
        print('total number of medias from this user: ' + str(len(self.full_media_list)))
        total_media_number = len(self.full_media_list)
        current_media_number = 0
        for media in self.full_media_list:
            current_media_number += 1
            print('getting tag from media: ' + media + '(' + str(current_media_number) +
                  '/' + str(total_media_number) + ')')
            tmp = self.get_tag_from_media(media)
            for tag in tmp:
                tag_list.append(tag)
        tag_list = Counter(tag_list).most_common()
        return tag_list

    def get_comment_from_user(self, name):
        media_list = self.get_media_from_user(name)
        full_comment_list = list()
        print('total number of medias from this user: ' + str(len(media_list)))
        for media in media_list:
            print('getting comments from media: ' + media)
            tmp = self.get_comment_from_media(media)
            for comment in tmp:
                full_comment_list.append(comment)
        return full_comment_list

    def get_all_comment_from_user(self, name):
        self.full_media_list = list()
        self.numPosts = 0
        self.get_user_full_media_data(name)
        full_comment_list = list()
        print('getting data for user: ' + name)
        print('total number of medias from this user: ' + str(len(self.full_media_list)))
        total_media_number = len(self.full_media_list)
        current_media_number = 0
        for media in self.full_media_list:
            current_media_number += 1
            print('getting tag from media: ' + media + '(' + str(current_media_number) +
                  '/' + str(total_media_number) + ')')
            tmp = self.get_comment_from_media(media)
            for comment in tmp:
                full_comment_list.append(comment)
        return full_comment_list

