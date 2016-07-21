from Instagram_Spider import *
import time
from sklearn import linear_model


spider = InstagramSpider()
sample_user_name = 'yy_god'
sample_private_user_name = 'sretiqa'
sample_public_user_name = 'silisunglasses'


# clf = linear_model.LinearRegression()
file = open('user_data.json', 'r')
data_list = json.load(file)
file.close()

for data in data_list:
    print(data)

print('end')
