from Instagram_Spider import *
import nltk


def store_tag_data(name, tag_data):
    file_name = name + '_tag_data.json'
    file = open(file_name, 'w')
    json.dump(tag_data, file)
    file.close()


def load_tag_data(name):
    file_name = name + '_tag_data.json'
    try:
        file = open(file_name, 'r')
        tag_data = json.load(file)
        file.close()
        return tag_data
    except FileExistsError:
        return None

categary_name = ['food', 'art', 'sport', 'technology', 'animal', 'life', 'location', 'others']
sample_media_code = 'BGUNUTcMhvo'
sample_user_name = 'yy_god'
sample_private_user_name = 'sretiqa'
sample_public_user_name = 'milafeitosa'


spider = InstagramSpider()
username = 'hongming0611'
password = 'zhm940330'
spider.login(username, password)


data = spider.get_all_tag_from_user(sample_public_user_name)
store_tag_data(sample_public_user_name, data)

print(data)
print('end')
