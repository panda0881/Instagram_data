from Instagram_Spider import instagram_spider

spider = instagram_spider()
username = 'hongming0611'
password = 'zhm940330'
sample_media_code = 'BGUNUTcMhvo'
spider.login(username, password)


# spider.get_user_media_data('megthelegend')
spider.get_tag_from_media(sample_media_code)

first_name = input('Please give me a tag name to start with: ')
tag_data = spider.get_tag_data(first_name)
for media in tag_data['top_posts']['nodes']:
    media_data = spider.get_media_data(media['code'])
    spider.user_list.append(media_data['owner']['username'])

print(spider.user_list)
print('end')
