from Instagram_Spider import *
import time


spider = InstagramSpider()
sample_user_name = 'yy_god'
sample_private_user_name = 'sretiqa'
sample_public_user_name = 'silisunglasses'

data = spider.get_user_data('hongming0611')
picture_url = data['profile_pic_url']
print(picture_url)
start_time = time.time()
tmp = requests.get('http://popularity.csail.mit.edu/cgi-bin/image.py?url=' + picture_url)
print('used time: ' + str(time.time() - start_time))
data2 = tmp.text.replace('\n', '')
score = json.loads(tmp.text)
print(score)
print('end')
