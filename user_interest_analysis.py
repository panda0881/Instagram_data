from Instagram_Spider import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from textblob import *
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from matplotlib import pyplot as plt


wordlist = set(words.words())
wordnet_lemmatizer = WordNetLemmatizer()
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')


def display_result(dict, confidence, username):
    plt.figure(figsize=(9, 9))
    labels = ['family', 'sport', 'animal', 'art', 'technology', 'life', 'fashion', 'food', 'travel']
    colors = ['green', 'blue', 'cyan', 'purple', 'orange', 'pink', 'seagreen', 'red', 'yellow']
    sizes = list()
    explode_list = list()
    max_label = ''
    current_value = 0
    total_value = 0
    for label in labels:
        sizes.append(dict[label])
        total_value += dict[label]
        if dict[label] > current_value:
            current_value = dict[label]
            max_label = label
    for label in labels:
        if label == max_label:
            explode_list.append(0.1)
        else:
            explode_list.append(0)
    final_sizes = list()
    for size in sizes:
        final_sizes.append(size/total_value)
    explode = tuple(explode_list)
    patches, l_text, p_text = plt.pie(final_sizes, explode=explode, labels=labels, colors=colors,
                                      autopct='%3.1f%%', shadow=False, startangle=90, pctdistance=0.7)
    for t in l_text:
        t.set_size = 12
    for t in p_text:
        t.set_size = 4
    plt.axis('equal')
    plt.text(-1.2, 1.1, 'username: ' + username, fontsize=15)
    plt.text(-1.2, 1, 'confidence: %.2f%%' % (confidence * 100), fontsize=15)
    plt.show()


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
        tag = clean_up_string(tag_pair[0]).lower()
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
            unsolved_list.append((tag, tag_pair[1]))
    print('done...')
    return result_list, unsolved_list


def analyze_words(words, dictionary):
    similarity_dictionary = dict()
    local_similarity_dictionary = dict()
    distribution_dictionary = dict()
    total_number = 0
    valid_word_count = 0
    for category in dictionary:
        similarity_dictionary[category] = 0
        local_similarity_dictionary[category] = 0
        distribution_dictionary[category] = list()
    distribution_dictionary['unknown'] = list()
    one_tenth = int(len(words)/10)
    current_number = 0
    progress = 0
    for word_pair in words:
        find_category = False
        current_number += 1
        if current_number > one_tenth:
            progress += 1
            current_number = 0
            print('finish ' + str(progress) + '0%')
        for category in dictionary:
            if word_pair[0] in dictionary[category]:
                valid_word_count += 1
                similarity_dictionary[category] += 10 * word_pair[1]
                distribution_dictionary[category].append(word_pair)
                find_category = True
                break
        if find_category:
            continue
        try:
            word = wn.synsets(word_pair[0])[0]
            total_number += word_pair[1]
            valid_word_count += 1
        except:
            continue
        for category in dictionary:
            word_list = dictionary[category]
            total_similarity = 0
            total_words = 0
            for test_word in word_list:
                try:
                    test = wn.synsets(test_word)[0]
                except:
                    continue
                try:
                    total_similarity += word.res_similarity(test, brown_ic)
                    total_words += 1
                except:
                    continue
            if total_words > 0:
                similarity_dictionary[category] += word_pair[1] * total_similarity / total_words
                local_similarity_dictionary[category] = total_similarity / total_words
        final_category = 'others'
        for category in local_similarity_dictionary:
            if local_similarity_dictionary[category] > local_similarity_dictionary[final_category]:
                final_category = category
        if local_similarity_dictionary[final_category] > 3:
            if local_similarity_dictionary[final_category] > 4:
                if word_pair[0] not in dictionary[final_category]:
                    dictionary[final_category].append(word_pair[0])
            find_category = True
            distribution_dictionary[final_category].append(word_pair)
        if not find_category:
            distribution_dictionary['unknown'].append(word_pair)
    for category in similarity_dictionary:
        similarity_dictionary[category] /= total_number
    rate = valid_word_count/len(words)
    percentage_dictionary = dict()
    total_words = 0
    for category in distribution_dictionary:
        percentage_dictionary[category] = 0
        for word_pair2 in distribution_dictionary[category]:
            percentage_dictionary[category] += word_pair2[1]
            total_words += word_pair2[1]
    for category in percentage_dictionary:
        percentage_dictionary[category] /= total_words
    print('done...')
    store_dictionary('Instagram_tag_dictionary.json', dictionary)
    return similarity_dictionary, rate, distribution_dictionary, percentage_dictionary


sample_media_code = 'BGUNUTcMhvo'
sample_user_name = 'yy_god'
sample_private_user_name = 'sretiqa'
sample_public_user_name = 'silisunglasses'
dictionary = load_dictionary('Instagram_tag_dictionary.json')
wordlist = combine_dictionary(wordlist, dictionary)
spider = InstagramSpider()
# username = 'hongming0611'
# password = input('hi, ' + username + 'please give me your password: ')
# spider.login(username, password)
data = get_data(spider, sample_public_user_name)
print('data got...')
print('analyzing tags from user: ' + sample_public_user_name)
words, unsolved_data = tag2word(data)
rate1 = successful_rate(words, unsolved_data)
print("successful rate of extracting from hashtag is：%.2f%%" % (rate1 * 100))
print('analyzing words from tags from user: ' + sample_public_user_name)
result, rate, distribute_result, percentage_result = analyze_words(words, dictionary)

print("successful rate of fitting words into dictionary is：%.2f%%" % (rate * 100))
print('similarity result: ')
print(result)
recognize_rate = 1-percentage_result['unknown']
print("our machine's current recognize rate is：%.2f%%" % (recognize_rate * 100))
print(distribute_result['unknown'])
display_result(percentage_result, recognize_rate, sample_public_user_name)
print('end')
