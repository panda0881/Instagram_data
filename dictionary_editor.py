import json


file_name = 'Instagram_tag_dictionary.json'
file = open(file_name, 'r')
data = json.load(file)
file.close()

print('end')