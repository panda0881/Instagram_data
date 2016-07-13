from Instagram_Spider import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from textblob import *
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic


wordlist = set(words.words())
wordnet_lemmatizer = WordNetLemmatizer()
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')


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


def analyze_words(words, dictionary):
    result_dictionary = dict()
    total_number = 0
    for category in dictionary:
        result_dictionary[category] = 0
    for word_pair in words:
        print('analyzing: ' + word_pair[0])
        total_number += word_pair[1]
        try:
            word = wn.synsets(word_pair[0])[0]
        except Exception:
            continue
        for category in dictionary:
            word_list = dictionary[category]
            if word_pair[0] in word_list:
                result_dictionary[category] += 1*word_pair[1]
            else:
                total_similarity = 0
                for test_word in word_list:
                    try:
                        test = wn.synsets(test_word)[0]
                    except Exception:
                        continue
                    try:
                        total_similarity += word.res_similarity(test, brown_ic)
                    except Exception:
                        continue
                result_dictionary[category] += word_pair[1]*total_similarity/len(word_list)
    for category in result_dictionary:
        result_dictionary[category] /= total_number
    return result_dictionary


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
dictionary = load_dictionary('Instagram_tag_dictionary.json')
result = analyze_words(words, dictionary)
print(result)

print('end')
