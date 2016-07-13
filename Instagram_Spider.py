import concurrent.futures
import json
import requests
import re
import os
from collections import Counter


def store_dictionary(dict_name, dict_data):
    file = open(dict_name, 'w')
    json.dump(dict_data, file)
    file.close()


def load_dictionary(dict_name):
    file = open(dict_name, 'r')
    dict_data = json.load(file)
    file.close()
    return dict_data


def list_formatting(input_list):
    list1 = Counter(input_list).most_common()
    output_list = list()
    for pair in list1:
        if pair[1] <= 1:
            break
        output_list.append(pair)
    return output_list


def strange_character_filter(input_string):
    if input_string is None:
        return ' '
    output_string = ''
    for character in input_string:
        if character != '\n':
            try:
                character.encode("gbk")
                output_string += character
            except UnicodeEncodeError:
                output_string = output_string
    return output_string


def store_tag_data(name, tag_data):
    file_name = name + '_tag_data.json'
    file = open(file_name, 'w')
    json.dump(tag_data, file)
    file.close()


def load_tag_data(name):
    file_name = name + '_tag_data.json'
    file = open(file_name, 'r')
    tag_data = json.load(file)
    file.close()
    return tag_data


def get_data(spider, name):
    file_name = name + '_tag_data.json'
    if os.path.isfile(file_name):
        tag_data = load_tag_data(name)
    else:
        tag_data = spider.get_all_tag_from_user(name)
        store_tag_data(name, tag_data)
    return tag_data


def successful_rate(successful_list, fail_list):
    successful_number = 0
    fail_number = 0
    for tag_pair in successful_list:
        successful_number += tag_pair[1]
    for tag_pair in fail_list:
        fail_number += tag_pair[1]
    rate = successful_number/(successful_number+fail_number)
    print("successful rate is：%.2f%%" % (rate * 100))


def clean_up_string(str):
    characters = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    newstring = ''
    for char in str:
        if char in characters:
            newstring += char
    return newstring.lower()


class InstagramSpider:
    def __init__(self):
        self.numPosts = 0
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self.future_to_item = {}
        self.s = requests.session()
        self.full_media_list = list()

    def login(self, username, password):
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
            'x-instagram-ajax': 1,
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

    def get_user_media_data(self, name):
        url = 'http://instagram.com/' + name + '/media'
        resp = requests.get(url)
        media = json.loads(resp.text)
        media_list = list()
        for item in media['items']:
            media_list.append(item['code'])
        return media_list

    def get_user_full_media_data(self, name, max_id=None):
        url = 'http://instagram.com/' + name + '/media'
        if max_id is not None:
            url += '?&max_id=' + max_id
        resp = requests.get(url)
        media = json.loads(resp.text)
        self.numPosts += len(media['items'])
        print('collecting data from ' + str(self.numPosts) + 'medias')
        for item in media['items']:
            self.full_media_list.append(item['code'])
        if 'more_available' in media and media['more_available'] is True:
            max_id = media['items'][-1]['id']
            self.get_user_full_media_data(name=name, max_id=max_id)

    def get_user_followers(self, name):
        resp = self.s.get('http://instagram.com/' + name + '/followers')
        tmp1 = resp.text[int(re.search('window._sharedData', resp.text).span()[1] + 3):]
        tmp2 = tmp1[:re.search('</script>', tmp1).span()[0] - 1]
        data = json.loads(tmp2)
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

    def download_user_media(self, name, max_id=None):
        url = 'http://instagram.com/' + name + '/media'
        if max_id is not None:
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

    def download(self, item, save_dir='./'):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        item['url'] = item[item['type'] + 's']['standard_resolution']['url']
        item['url'] = re.sub(r'/s\d{3,}x\d{3,}/', '/', item['url'])
        base_name = item['url'].split('/')[-1].split('?')[0]
        file_path = os.path.join(save_dir, base_name)
        with open(file_path, 'wb') as file:
            bytes = requests.get(item['url']).content
            file.write(bytes)

        file_time = int(item['created_time'])
        os.utime(file_path, (file_time, file_time))

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
                        pos = l[l.index(0)+1]
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

    def get_media_from_tag(self, tag_name):
        media_list = list()
        data = self.get_tag_data(tag_name)
        for media in data['top_posts']['nodes']:
            media_list.append(media['code'])
        for media in data['media']['nodes']:
            media_list.append(media['code'])
        media_list = list(set(media_list))
        return media_list

    def get_user_from_media(self, media_code):
        data = self.get_media_data(media_code)
        user_list = list()
        user_list.append(data['owner']['username'])
        for comment in data['comments']['nodes']:
            user_list.append(comment['user']['username'])
        # for like in data['likes']['nodes']:
        #     user_list.append(like['user']['username'])
        user_list = list(set(user_list))
        return user_list

    def get_user_from_tag(self, tag_name):
        medias = self.get_media_from_tag(tag_name)
        user_list = list()
        for media in medias:
            tmp = self.get_user_from_media(media)
            for user in tmp:
                user_list.append(user)
        user_list = list(set(user_list))
        final_user_list = list()
        for user in user_list:
            data = self.get_user_data(user)
            if data['is_private'] == False and data['followed_by']['count'] > 500:
                final_user_list.append(user)
        return final_user_list

    def get_tag_from_user(self, name):
        media_list = self.get_user_media_data(name)
        tag_list = list()
        print('total number of medias from this user: ' + str(len(media_list)))
        for media in media_list:
            print('getting tag from media: ' + media)
            tmp = self.get_tag_from_media(media)
            for tag in tmp:
                tag_list.append(tag)
        tag_list = list_formatting(tag_list)
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
