from Instagram_Spider import *
import time
from sklearn import linear_model
from pandas import Series, DataFrame
import pandas as pd
from sklearn import svm


spider = InstagramSpider()
sample_user_name = 'yy_god'
sample_private_user_name = 'sretiqa'
sample_public_user_name = 'silisunglasses'

file = open('train_data.json', 'r')
train_data = json.load(file)
file.close()
file = open('test_data.json', 'r')
test_data = json.load(file)
file.close()

my_frame = DataFrame(train_data)
training_result = list(my_frame['likes_result'])
del my_frame['likes_result']
del my_frame['is_verified']
del my_frame['username']
del my_frame['comments_result']
del my_frame['follows_number']
del my_frame['comments_number']
del my_frame['biography_length']
del my_frame['posts_number']
del my_frame['info_number']
training_set = list()
print(my_frame)
for number in range(0, 600):
    tmp = my_frame.ix[number]
    training_set.append(list(tmp))

my_test_frame = DataFrame(test_data)
test_result = list(my_test_frame['likes_result'])
del my_test_frame['likes_result']
del my_test_frame['is_verified']
del my_test_frame['username']
del my_test_frame['comments_result']
del my_test_frame['follows_number']
del my_test_frame['comments_number']
del my_test_frame['biography_length']
del my_test_frame['posts_number']
del my_test_frame['info_number']
test_set = list()
for number in range(0, 200):
    tmp = my_test_frame.ix[number]
    test_set.append(list(tmp))

clf = linear_model.LinearRegression(fit_intercept=False)
clf.fit(training_set, training_result)
predict_result = clf.predict(test_set)
score = clf.score(test_set, test_result)

print(test_set)
print('coeficient: ')
print(clf.coef_)
print('Real result: ')
print(test_result)
print('Predict result: ')
print(predict_result)
print('Score: ')
print(score)

print('end')
