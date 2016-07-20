from Instagram_Spider import *
import csv
import time
field_names = ['username', 'picture_score', 'info_number', 'biography_length', 'comments_number', 'likes_number',
               'followers_number', 'follows_number', 'posts_number', 'tags_number']
user_list = ['hongming0611', 'yy_god', 'silisunglasses']
spider = InstagramSpider()


my_file = open('influence_analysis_data', 'w', newline='')
my_writer = csv.writer(my_file)
my_writer.writerow(field_names)
my_file.close()

for user in user_list:
    data = spider.get_user_data(user)
    picture_url = data['profile_pic_url']
    if data['']
    biography_length = len(data[])
    print(data)

print('end')
