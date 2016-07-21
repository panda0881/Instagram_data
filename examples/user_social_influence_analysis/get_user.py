from Instagram_Spider import *

spider = InstagramSpider()

start_user = 'alfusofilm'
follower_list, follow_list = spider.get_user_followers_and_follows(start_user)
final_list = list()
for user in follow_list:
    if len(final_list) >= 1000:
        break
    data = spider.get_user_data(user)
    if not data['is_private'] and data['media']['count'] > 20:
        final_list.append(user)
        print('Current database size is: ' + str(len(final_list)))
for user in follower_list:
    if len(final_list) >= 1000:
        break
    data = spider.get_user_data(user)
    if not data['is_private'] and data['media']['count'] > 20:
        final_list.append(user)
        print('Current database size is: ' + str(len(final_list)))

file = open('user_list.json', 'w')
json.dump(final_list, file)
file.close()

print('end')
