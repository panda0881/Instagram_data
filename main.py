from Instagram_Spider import instagram_spider
import time

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

print(result)
print('end')
