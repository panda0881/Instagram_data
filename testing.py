from Instagram_Spider import instagram_spider

sample_user_name = 'megthelegend'
spider = instagram_spider()
username = 'hongming0611'
password = 'zhm940330'
sample_media_code = 'BGUNUTcMhvo'
spider.login(username, password)

data = spider.get_user_data(sample_user_name)

print('end')