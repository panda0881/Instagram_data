Instagram_data 
============================================================
(A non-API Instagram data collector)
---------

The first reason for me to start this project is that I want to collect some useful data about an Instagram tag and there is no current solution solving this problem, so I decide to develop my own library to crawl some data from the Instagram.
After I finish collecting data about tags, I moved to build data-crawler for Instagram user as well as Instagram media, thus you can combine those as you want and develop your own Instagram-crawler.

----------
Advantages:
---------
1.	Python 3.5: I am using python 3.5 to finish this task. As scrapy is still not fully supported for python 3.5 for now. If you want to do some crawling with python 3.5, you should try this out.
2.	Non-API: Instead of using official API to get data, I choose to use the old-school way. Thus you don’t need to register as developer to use this library
3.	Higly-open: The Instagram_data library offers multiple functions to collect different data from the Instagram. You are free to use them for your own interest and develop your own program

Features:
---------
1.	Getting data from user:
Input is username of this specific user
Output is a JSON file containing the following information about this user: username, full name, biography, number of follows, number of followed-by, list of media... 
2.	Getting data from media:
Input is the media code of this specific media
Output is a JSON file containing the following information about this media: data about comments, data about likes, data about owner...
3.	Getting data from tag:
Input is the name of this tag
Output is a JSON file containing the following information about this tag: the static media list
4.	Download user’s media:
Input is the name of this specific user
Output is a folder that store all the media about this specific user
5.	Log-in:
Input is your own user name and password for Instagram and thus the scraper can login as you and store the data

To-do list:
---------
1.	Collecting data about user’s follower and following list
2.	Collecting data about the full media list of a tag
3.	Developing a mechanism to evaluate the social influence power of a specific user based on his medias
4.	Developing a mechanism to filter all the tags about a user to find out his interest area
5.	Using all the tags existing in a specific user's posts to analyze his interest area

Remarks:
---------
1. Great thanks to rarcega, whose project (https://github.com/rarcega/instagram-scraper) gave me the first hint of collecting data from Instagram without API.
2. As the full media list of a tag and the following and follower list are loaded with javascript, I have to find another way to solve this problem.
3. Your help is more than welcomed

