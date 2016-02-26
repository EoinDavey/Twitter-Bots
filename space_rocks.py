#!/usr/bin/env/ python
# -*- coding: utf-8 -*-

import tweepy, traceback, urllib, json, HTMLParser, string

CONSUMER_KEY = "#consumer key"
CONSUMER_SECRET = "#consumer secret"
ACCESS_KEY="#access key"
ACCESS_SECRET="#access secret"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, secure=True)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class listener(tweepy.StreamListener):
	def on_status(self, status):
		process_status(status)
	def on_error(self, status):
		print "Error code " + str(status)
	
def process_status(status):
	status_text = filter(lambda x: x in string.printable, status.text)
	strings = status_text.split()
	if(strings[0] != "RT" and status.user.screen_name == "astro_timpeake"):
		print "valid"
		song_search(status_text, status.id,status.user.screen_name)
	elif(strings[0] == "RT"):
		return
	elif(status.user.screen_name != "astro_timpeake"):
		return

def song_search(lyrics, id,user):
	lyrics = lyrics.replace("#spacerocks.3", "",1)
	search_term = lyrics + " " + "site:azlyrics.com"
	print "Search Term:" + search_term
	url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&"
	query = urllib.urlencode({"q": search_term})
	response = urllib.urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	json_response = json.loads(response)
	results = json_response["responseData"]["results"]
	if(len(results) == 0):
		return
	escaped_title = results[0]["titleNoFormatting"]
	if(len(escaped_title) == 0):
		return
	h = HTMLParser.HTMLParser()
	title = h.unescape(escaped_title)
	terms = title.split()
	artist = ""
	song_title = ""
	i = 0
	failed = False
	length = len(terms)
	while True:
		if(terms[i].lower() == "lyrics"):
			break
		elif(terms[i] == "-"):
			failed = True
			break
		elif(i>= length):
			failed=True
			break
		else:
			artist += (" " + terms[i])
		i+=1
	i+=1
	if(terms[i] == "-"):
		i+=1
		while True:
			if(terms[i] == "-"):
				break
			else:
				song_title += (terms[i] + " ")
			i+=1
	if(failed==False):
		artist = artist.title()
		print "Title: " + song_title + " Artist: " + artist
		reply(song_title, artist, id, user)
	else:
		print "Failed lookup"

def reply(title, artist, id, user):
	try:
		api.update_status("@astro_timpeake " + title + "by" + artist + " #spacerocks", id)
	except:
		pass
		print traceback.format_exc()
		
l = listener()
stream = tweepy.Stream(auth, l)
stream.filter(follow=["552582271"])
