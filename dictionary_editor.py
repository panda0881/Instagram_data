import json
from Instagram_Spider import *


def store_dictionary(dict_name, dict_data):
    file = open(dict_name, 'w')
    json.dump(dict_data, file)
    file.close()


def load_dictionary(dict_name):
    file = open(dict_name, 'r')
    dict_data = json.load(file)
    file.close()
    return dict_data


def delete_word(dictionary):
    category = input('category:')
    if category not in dictionary.keys():
        print('there is no such category for now...')
        return dictionary
    word = input('word:')
    if word not in dictionary[category]:
        print('There is no word ' + word + 'in category:' + category)
        return dictionary
    dictionary[category].remove(word)
    return dictionary


def add_word(dictionary):
    category = input('category:')
    if category not in dictionary.keys():
        print('there is no such category for now...')
        return dictionary
    word = input('word:')
    if word in dictionary[category]:
        print('We have already had' + word + 'in category:' + category)
        return dictionary
    dictionary[category].append(word)
    print()
    return dictionary


def main():
    dictionary = load_dictionary('Instagram_tag_dictionary.json')
    while True:
        print('what do you want to do?(a: add word to the dictionary; d: delete word from the dictionary; q:quit!)')
        command = input('command:')
        if command == 'a':
            dictionary = add_word(dictionary)
        elif command == 'd':
            dictionary = delete_word(dictionary)
        elif command == 'q':
            store_dictionary('Instagram_tag_dictionary.json', dictionary)
            break
        else:
            print('please input a valid command')
    print(dictionary)
    print('end')

if __name__ == '__main__':
    main()
