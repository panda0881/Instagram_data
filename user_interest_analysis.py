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


def combine_dictionary(official_wordlist, my_dictionary):
    official_wordlist1 = list(official_wordlist)
    for category in my_dictionary:
        word_list = my_dictionary[category]
        for word in word_list:
            official_wordlist1.append(word)
    official_wordlist2 = set(official_wordlist1)
    return official_wordlist2


def tag2word(tag_list):
    result_list = list()
    unsolved_list = list()
    one_tenth = int(len(tag_list)/10)
    current_number = 0
    progress = 0
    for tag_pair in tag_list:
        current_number += 1
        if current_number > one_tenth:
            progress += 1
            current_number = 0
            print('finish ' + str(progress) + '0%')
        tag = tag_pair[0]
        tag = clean_up_string(tag)
        pos = len(tag)
        while pos > 1:
            word = wordnet_lemmatizer.lemmatize(tag[0:pos])
            if word in wordlist:
                result_list.append((word, tag_pair[1]))
                tag = tag[pos:]
                pos = len(tag)
            else:
                pos -= 1
        if len(tag) > 1:
            tag = Word(tag).correct()
            word = wordnet_lemmatizer.lemmatize(tag)
            if word in wordlist:
                result_list.append((word, tag_pair[1]))
            else:
                unsolved_list.append((tag, tag_pair[1]))
    print('done...')
    return result_list, unsolved_list


def analyze_words(words, dictionary):
    result_dictionary = dict()
    total_number = 0
    valid_word_count = 0
    for category in dictionary:
        result_dictionary[category] = 0
    one_tenth = int(len(words)/10)
    current_number = 0
    progress = 0
    for word_pair in words:
        current_number += 1
        if current_number > one_tenth:
            progress += 1
            current_number = 0
            print('finish ' + str(progress) + '0%')
        try:
            word = wn.synsets(word_pair[0])[0]
            total_number += word_pair[1]
            valid_word_count += 1
        except Exception:
            continue
        for category in dictionary:
            word_list = dictionary[category]
            total_words = 0
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
                        total_words += 1
                    except Exception:
                        continue
                if total_words > 0:
                    result_dictionary[category] += word_pair[1]*total_similarity/total_words
    for category in result_dictionary:
        result_dictionary[category] /= total_number
    rate = valid_word_count/len(words)
    print('done...')
    return result_dictionary, rate


sample_media_code = 'BGUNUTcMhvo'
sample_user_name = 'yy_god'
sample_private_user_name = 'sretiqa'
sample_public_user_name = 'silisunglasses'
dictionary = load_dictionary('Instagram_tag_dictionary.json')
wordlist = combine_dictionary(wordlist, dictionary)
spider = InstagramSpider()
# username = 'hongming0611'
# password = 'zhm940330'
# spider.login(username, password)
data = get_data(spider, sample_public_user_name)
print('data got...')
print('analyzing tags from user: ' + sample_public_user_name)
words, unsolved_data = tag2word(data)
successful_rate(words, unsolved_data)

print('analyzing words from tags from user: ' + sample_public_user_name)
result, rate = analyze_words(words, dictionary)
print(result)
print("successful rate is：%.2f%%" % (rate * 100))

print('end')
