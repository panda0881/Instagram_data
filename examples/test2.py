from Instagram_Spider import *

tag_name = 'skate2work'

spider = InstagramSpider()
data = spider.get_tag_data(tag_name)
data2 = spider.get_user_data('hongming0611')
top_list, full_list = spider.get_media_from_tag(tag_name)

print('end')
