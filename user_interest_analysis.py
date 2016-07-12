from Instagram_Spider import *
import nltk

categary_name = ['food', 'art', 'sport', 'technology', 'animal', 'life', 'location', 'others']
sample_media_code = 'BGUNUTcMhvo'
sample_user_name = 'yy_god'
sample_private_user_name = 'sretiqa'
sample_public_user_name = 'milafeitosa'

spider = InstagramSpider()
username = 'hongming0611'
password = 'zhm940330'
spider.login(username, password)
data = get_data(sample_public_user_name)


print('end')
