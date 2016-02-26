#!/usr/bin/env/ python
# -*- coding: utf-8 -*-

import tweepy, time, os.path, thread, random, traceback
from subprocess import call

CONSUMER_KEY = "#consumer secret"
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

class mentionsListener(tweepy.StreamListener):
	def on_status(self, status):
		process_mention(status)
	def on_error(self, status):
		print "Error code " + str(status)

def process_mention(status):
	print status.user.screen_name + ": " + status.text
	if(status.user.screen_name == "EnemyOfAFriend"):
		try:
			api.update_status("@" + status.user.screen_name + " Gib me da moneh", status.id)
			print "Replied to Luc"
		except:
			pass
			print "Error replying to Luc"
	elif(status.user.screen_name != "AngryStormcloak"):
		try:
			api.update_status("@" + status.user.screen_name + " " + random.choice(mentions_quote), status.id)
			print "Replied to message"
		except:
			pass
			print traceback.format_exc()
	
def process_status(status):
	print  status.user.screen_name + ":  " + status.text
	strings = status.text.split()
	if(strings[0] != "RT" and status.user.screen_name != "AngryStormcloak"):
		try:
			api.update_status("@" + status.user.screen_name + " " + random.choice(nords_quote),status.id)
			print "Replied"
		except:
			pass
			print traceback.format_exc()
	elif(strings[0] == "RT"):
		print "Retweeted Status"
	elif(status.user.screen_name == "AngryStormcloak"):
		print "Self tweet"

def check_mentions():
	listener = mentionsListener()
	stream = tweepy.Stream(auth,listener)
	stream.filter(track=["@AngryStormcloak"])
		
l = listener()
stream = tweepy.Stream(auth, l)
thread.start_new_thread(check_mentions,())
stream.filter(track=["nords", "imperials"], languages=["en"])
stream.filter(follow=["108054718"])
