**Instagram_data** 
============================================================

*It is a non-API Instagram spider. To use it, you don't need the official Instagram API and all you need is a normal Instagram account for login usage.*

----------
Advantages:
---------
1.	Python 3.5: I am using python 3.5 to develop this spider. As [Scrapy](http://scrapy.org/) is still not fully supported for python 3.5 for now. If you want to do some crawling with python 3.5, you should try this out.
2.	Non-API: Instead of using official API to access data, I choose to use the old-school way. Thus you don’t need to register as developer to use this library.
3.	Fully-functional: Every data you can find from Instagram through browser, you can get access to it with this InstagramSpider. For instance, you can get access to all the data about the users, the hash tags as well as all the medias.
4.	Highly-open: The Instagram_data library offers multiple functions to collect different data from the Instagram. You are free to use them for your own interest and develop your own program based on it.

Document:
---------
 1. **Library used:**
The following libraries are used in this spider: concurrent.features, json, requests, re, os, collections

 2. **Main method usage and introduction:**
 
 1.`login(self, username, password):`

 This method is used for log-in activity. The input value of this method is your own personal Instagram username and password and spider will keep the log-in state through this method.

 2.`get_user_data(self, name):` 
 
 The input of this method is the username you are interested in.
 The output of this method is a [JSON](http://www.json.org/) file containing all the personal information about this specific user.
 
 3.`get_tag_data(self, tag_name):`
 
 The input of this method is the name of the tag you are interested in.
 The output of this method is a [JSON](http://www.json.org/) file containing all the data about this specific tag.
 
 4.`get_media_data(self, media_code):`
 
 The input of this method is the code of the media you are interested in.
 The output of this method is a [JSON](http://www.json.org/) file containing all the data about this specific media.
 
 5.`get_user_followers_and_follows(self, name):`
 
 The input of this method is the username you are interested in.
 The output of this method are two lists. The first one is the follower list of this specific user, while the second one is the follow list of this specific user.
 
 6.`download_user_media(self, name, max_id=None):`
 
 The input of this method is the username you are interested in and this method will download and store all of the medias that belong to this specific user to a folder named by the user's name.
 
 7.`get_tag_from_media(self, media_code):`
 
 The input of this method is the media code you are interested in.
 The output of this method is a list containing all the tags appearing in this media.
 
 8.`get_media_from_tag(self, tag_name):`
 
 The input of this method is the tag name you are interested in.
 The output of this method are two lists. The first one contains all the media codes belong to top_post under this tag, while the second one is the full list of all the media codes under this tag.
 
 9.`get_user_from_media(self, media_code):`
 
 The input of this method is the media code you are interested in.
 The output of this method is a list containing all the username who is active under this media.
 
 10.`get_media_from_user(name):`
 
 The input of this method is the username you are interested in.
 The output of this method is a list containing the first 20 media codes of this user.
 
 11.`get_user_from_tag(self, tag_name):`
 
 The input of this method is the tag name you are interested in.
 The output of this method is a list containing all the username who is related to this tag through media.
 
 12.`get_all_tag_from_user(self, name):`
 
 The input of this method is the username you are interested in.
 The output of this method is a list containing all the tags appearing in this user's medias.
 
 13.`get_tag_from_user(self, name):` (shorter version of the above one)
 
 The input of this method is the username you are interested in.
 The output of this method is a list containing all the tags appearing in this user's first 20 medias.
 
 
 
 3. **Reminders:**
 
 1.For the function that require log-in (like getting follower and follow list or collect media from a tag), you may need to log-in first.

 2.For the cookie part I used in this class, you may need to renew it. 
 PS: you can get that through your browser
 

Examples:
---------
**I am trying to employ this spider to do some funny work. If possible, I will post those program and testing result into the example folder. Current sample project plan is as following:**

1.	Develop a mechanism to evaluate the social influence power of a specific user based on his medias

2.	Develop a mechanism to evaluate the interest distribution of a specific user based on his tags and maybe comments. (Using NLP)

3.	Develop a mechanism to study the relationship between different tags


Remarks:
---------
1. Great thanks to rarcega, whose project (https://github.com/rarcega/instagram-scraper) gave me the first hint of collecting data from Instagram without API.
2. You are free to use this spider on your own responsibility.
3. Your help is more than welcomed
4. If you want to see some examples using this spider, you can check the following project: Instagram_spider_application (https://github.com/panda0881/Instagram_spider_application)

Licence:
--------
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007
