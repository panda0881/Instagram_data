from Instagram_Spider import *
import time
import csv


def record_info(tag_dict, spider, file_name):
    my_file = open(file_name, 'a', newline='')
    my_writer = csv.writer(my_file)
    for user in tag_dict:
        data = spider.get_user_data(user)
        tags = tag_dict[user]
        tag_string = ''
        for tag in tags:
            tag_string = tag_string + '#' + tag[0] + ':' + str(tag[1]) + ' '
        tag_string = strange_character_filter(tag_string)
        row = [strange_character_filter(user), data['is_private'],
               strange_character_filter(data['full_name']), strange_character_filter(data['biography']),
               data['followed_by']['count'], tag_string]
        try:
            my_writer.writerow(row)
        except UnicodeEncodeError:
            print('There is something wrong with the data about' + user)
    my_file.close()


def main():
    start_time = time.time()
    spider = InstagramSpider()
    username = 'hongming0611'
    password = 'zhm940330'
    spider.login(username, password)
    field_names = ['username', 'is private', 'fullname', 'biography', 'followed by', 'tags']
    result = dict()

    first_name = input('Please give me a tag name to start with: ')
    file_name = 'Instagram_' + first_name + '_data.csv'
    my_file = open(file_name, 'w', newline='')
    my_writer = csv.writer(my_file)
    my_writer.writerow(field_names)
    my_file.close()
    users = spider.get_user_from_tag(first_name)
    print('finish getting user data...')
    print('total user number: ' + str(len(users)))
    print('used time: ' + str(time.time() - start_time))
    for user in users:
        print('getting data for user: ' + user)
        result[user] = spider.get_tag_from_user(user)
        print('used time: ' + str(time.time() - start_time))
    record_info(tag_dict=result, spider=spider, file_name=file_name)
    print('end')

if __name__ == '__main__':
    main()
