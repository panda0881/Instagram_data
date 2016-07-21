from Instagram_Spider import *
import csv
import json


def store_data(dict_name, dict_data):
    file = open(dict_name, 'w')
    json.dump(dict_data, file)
    file.close()


def load_data(dict_name):
    file = open(dict_name, 'r')
    dict_data = json.load(file)
    file.close()
    return dict_data

field_names = ['username', 'is_verified', 'info_number', 'biography_length', 'comments_number',
               'likes_number', 'followers_number', 'follows_number', 'posts_number', 'tags_number', 'comments_result',
               'likes_result']
user_list = load_data('user_list.json')
current_data = load_data('user_data.json')
spider = InstagramSpider()


def get_user_data(user):
    data_dict = dict()
    data = spider.get_user_data(user)
    data_dict['picture_url'] = data['profile_pic_url']
    if data['biography']:
        data_dict['biography_length'] = len(data['biography'])
    else:
        data_dict['biography_length'] = 0
    data_dict['full_name'] = data['full_name']
    data_dict['country_block'] = data['country_block']
    data_dict['external_url'] = data['external_url']
    info_number = 0
    for data_type in data_dict:
        if data_dict[data_type] and data_dict[data_type] != 0:
            info_number += 1
    data_dict['info_number'] = info_number
    data_dict['posts_number'] = data['media']['count']
    data_dict['followers_number'] = data['followed_by']['count']
    data_dict['follows_number'] = data['follows']['count']
    if data['is_verified']:
        data_dict['is_verified'] = 1
    else:
        data_dict['is_verified'] = 0
    media_list = spider.get_media_from_user(user)
    comments_number = 0
    likes_number = 0
    current_number = 0
    for media in media_list[:4]:
        current_number += 1
        print('analyzing user media: ' + media + '(' + str(current_number) + '/20)')
        media_data = spider.get_media_data(media)
        comments_number += media_data['comments']['count']
        likes_number += media_data['likes']['count']
    data_dict['comments_result'] = comments_number / 4
    data_dict['likes_result'] = likes_number / 4
    comments_number = 0
    likes_number = 0
    tags_number = 0
    for media in media_list[4:]:
        current_number += 1
        print('analyzing user media: ' + media + '(' + str(current_number) + '/20)')
        media_data = spider.get_media_data(media)
        comments_number += media_data['comments']['count']
        likes_number += media_data['likes']['count']
        tags_list = spider.get_tag_from_media(media)
        tags_number += len(tags_list)
    data_dict['comments_number'] = comments_number / 16
    data_dict['likes_number'] = likes_number / 16
    data_dict['tags_number'] = tags_number / 16
    data_dict['username'] = user
    del data_dict['external_url']
    del data_dict['full_name']
    del data_dict['country_block']
    del data_dict['picture_url']
    return data_dict

start_number = 595
end_number = 1000

for user in user_list[start_number:end_number + 1]:
    print('Collecting data for user: ' + user)
    user_data_dict = get_user_data(user)
    current_data.append(user_data_dict)
    print('Total data number: ' + str(len(current_data)))
    store_data('user_data.json', current_data)

print('end')








