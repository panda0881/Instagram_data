from Instagram_Spider import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from textblob import *
from nltk.corpus import wordnet

wordlist = set(words.words())
wordnet_lemmatizer = WordNetLemmatizer()


def tag2word(tag_list):
    result_list = list()
    unsolved_list = list()
    total_number = len(tag_list)
    current_number = 0
    for tag_pair in tag_list:
        current_number += 1
        print('analyzing: ' + tag_pair[0] + '(' + str(current_number) + '/' + str(total_number) + ')')
        tag = tag_pair[0]
        tag = clean_up_string(tag)
        pos = len(tag)
        while pos > 1:
            word = wordnet_lemmatizer.lemmatize(tag[0:pos])
            if word in wordlist:
                print(word)
                result_list.append((word, tag_pair[1]))
                tag = tag[pos:]
                pos = len(tag)
            else:
                pos -= 1
        if len(tag) > 1:
            tag = Word(tag).correct()
            word = wordnet_lemmatizer.lemmatize(tag)
            print(tag)
            if word in wordlist:
                result_list.append((word, tag_pair[1]))
            else:
                unsolved_list.append((tag, tag_pair[1]))
    return result_list, unsolved_list

categary_name = ['food', 'art', 'sport', 'technology', 'animal', 'life', 'location', 'others']
sample_media_code = 'BGUNUTcMhvo'
sample_user_name = 'yy_god'
sample_private_user_name = 'sretiqa'
sample_public_user_name = 'silisunglasses'
teststring = 'thisisabird'

spider = InstagramSpider()
# username = 'hongming0611'
# password = 'zhm940330'
# spider.login(username, password)
data = get_data(spider, sample_public_user_name)
print('data got...')
words, unsolved_data = tag2word(data)
successful_rate(words, unsolved_data)
print(unsolved_data)

print('end')
