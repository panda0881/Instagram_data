from Instagram_Spider import *
import time
import csv


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
        row = [strange_character_filter(user), strange_character_filter(data['country_block']),
               strange_character_filter(data['full_name']), strange_character_filter(data['biography']),
               data['followed_by']['count'], tag_string]
        try:
            my_writer.writerow(row)
        except UnicodeEncodeError:
            print('There is something wrong with the data about ' + user)
    my_file.close()


def main():
    start_time = time.time()
    spider = InstagramSpider()
    username = 'hongming0611'
    password = input('hi, ' + username + 'please give me your password: ')
    spider.login(username, password)
    field_names = ['username', 'location', 'fullname', 'biography', 'followed by', 'tags']
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
