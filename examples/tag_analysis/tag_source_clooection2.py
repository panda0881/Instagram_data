from Instagram_Spider import *
import time
import csv


def record_info(tag_dict, spider, file_name):
    my_file = open(file_name, 'a', newline='')
    my_writer = csv.writer(my_file)
    for user in tag_dict:
        tags = tag_dict[user]
        for tag in tags:
            tag_name = strange_character_filter(tag[0])
            row = [tag_name]
            try:
                my_writer.writerow(row)
            except UnicodeEncodeError:
                print('There is something wrong with the data about ' + user)
    my_file.close()


def main():
    start_time = time.time()
    spider = InstagramSpider()
    username = 'hongming0611'
    password = 'zhm940330'
    spider.login(username, password)
    field_names = ['tags']
    result = dict()

    first_name = input('Please give me a tag name to start with: ')
    file_name = 'Instagram_' + first_name + '_data2.csv'
    my_file = open(file_name, 'w', newline='')
    my_writer = csv.writer(my_file)
    my_writer.writerow(field_names)
    my_file.close()
    users = spider.get_user_from_tag(first_name)
    print('finish getting user data...')
    print('total user number: ' + str(len(users)))
    print('used time: ' + str(time.time() - start_time))
    total_user_number = len(users)
    current_user_number = 0
    for user in users:
        current_user_number += 1
        print('getting data for user: ' + user + '(' + str(current_user_number) + '/' + str(total_user_number) + ')')
        result[user] = spider.get_tag_from_user(user)
        print('used time: ' + str(time.time() - start_time))
    record_info(tag_dict=result, spider=spider, file_name=file_name)
    print('end')

if __name__ == '__main__':
    main()
