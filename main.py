from Instagram_Spider import instagram_spider
import time
import csv


def strange_character_filter(input_string):
    output_string = ''
    for character in input_string:
        if character != '\n':
            try:
                character.encode("gbk")
                output_string += character
            except UnicodeEncodeError:
                print('find a strange character')
    return output_string


def record_info(dict, spider, original_tag):
    field_names = ['original tag', 'username', 'fullname', 'biography', 'isprivate', 'follows', 'followed by', 'url', 'tag']
    my_file = open('Instagram_tag_data.csv', 'w', newline='')
    my_writer = csv.writer(my_file)
    my_writer.writerow(field_names)
    for user in dict:
        data = spider.get_user_data(user)
        tags = dict[user]
        tag_string = ''
        for tag in tags:
            tag_string = tag_string + '#' + tag + ' '
        tag_string = strange_character_filter(tag_string)
        url = 'http://instagram.com/' + user
        row = [original_tag, strange_character_filter(user), strange_character_filter(data['full_name']),strange_character_filter(data['biography']), data['is_private'], data['follows']['count'], data['followed_by']['count'], url, tag_string]
        my_writer.writerow(row)
    my_file.close()

start_time = time.time()
spider = instagram_spider()
username = 'hongming0611'
password = 'zhm940330'
sample_media_code = 'BGUNUTcMhvo'
sample_user_name = 'yy_god'
spider.login(username, password)
result = dict()

first_name = input('Please give me a tag name to start with: ')
users = spider.get_user_from_tag(first_name)
print('finish getting user data...')
print('total user number: ' + str(len(users)))
print('used time: ' + str(time.time()-start_time))
for user in users:
    print('getting data for user: ' + user)
    result[user] = spider.get_tag_from_user(user)
    print('used time: ' + str(time.time() - start_time))

record_info(dict=result, spider=spider, original_tag=first_name)
print('end')
