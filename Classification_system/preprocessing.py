#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import nltk
import string
from extract_tweets import get_tweet_map, get_id_tokenised_tweet_map, get_stop_words

global n_for_char, n_for_word
n_for_char = 3
n_for_word = 5

all_emoticons = \
	[	':-)', ':)', '(:', '(-:',\
		':-D', ':D', 'X-D', 'XD', 'xD',\
		'<3', ':\*',\
		';-)', ';)', ';-D', ';D', '(;', '(-;',\
		':-(', ':(',\
		':,(', ':\'(', ':"(', ':((',\
		':-P', ':P', ':p', ':-p',\
	]

# Get emoticons from a tweet.
def getemoticons(tweet):
	emoticons = []
	for emoticon in all_emoticons:
		if emoticon in tweet:
			emoticons.append(emoticon)
	return emoticons

# Get hashtags from a tweet.
def gethashtags(tokenized_tweet):
	hashtags = []
	for token in tokenized_tweet:
		if token[0] == '#':
			hashtags.append(token.lower())
	return hashtags

# Get mentions from a tweet.
def getmentions(tokenized_tweet):
	mentions = []
	for token in tokenized_tweet:
		if token[0] == '@':
			mentions.append(token)
	return mentions

# Get URLs from a tweet.
def geturls(tweet):
	url_regex = [r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+']
	url_re = re.compile(r'('+'|'.join(url_regex)+')', re.VERBOSE | re.IGNORECASE)
	urls = url_re.findall(tweet)
	return urls

# Get character n-grams (n=1-3) for a tweet.
def getcharngrams(tweet):
	char_n_grams = []
	for i in xrange(1, n_for_char + 1):
		char_i_grams = [tweet[j:j+i] for j in xrange(len(tweet)- (i-1))]
		char_n_grams.extend(char_i_grams)
	return char_n_grams

# Filter a tweet by replacing the original hashtags, mentions, URLs and emoticons and removing punctuations, stop-words.
def processtweet(tokenized_tweet, stop_words):
	processed_tweet = []

	for i in xrange(len(tokenized_tweet)):
		if tokenized_tweet[i][0] == '#':
			processed_tweet.append(tokenized_tweet[i][1:])
		elif tokenized_tweet[i][0] == '@' or tokenized_tweet[i][0] in string.punctuation:
			continue
		elif tokenized_tweet[i].lower() in stop_words:
			continue
		elif 'http' in tokenized_tweet[i]:
			continue
	for i in xrange(len(processed_tweet)):
		processed_tweet[i] = processed_tweet[i].lower()
	return processed_tweet

# Get word n-grams (n=1-5) for a tweet.
def getwordngrams(processed_tokenized_tweet):
	word_n_grams = []
	for i in xrange(1, n_for_word + 1):
		word_i_grams = [" ".join(processed_tokenized_tweet[j:j+i]) for j in xrange(len(processed_tokenized_tweet) - (i-1))]
		word_n_grams.extend(word_i_grams)
	return word_n_grams

# Get count of all punctuations in a tweet.
def getpunctuations(processed_tweet):
	pucntuations_count = {}

	for char in processed_tweet:
		if char in all_punctuations:
			if char in pucntuations_count:
				pucntuations_count[char] += 1
			else:
				pucntuations_count[char] = 1
	return pucntuations_count

# Extract all the features of a tweet and create a feature vector.
def preprocess(key, tweet):
	id_tweet_map, tweet_id_map = get_tweet_map()
	id_tokenised_tweet_map = get_id_tokenised_tweet_map()
	
	tokenized_tweet = id_tokenised_tweet_map[key]
	
	# Get emoticons, hashtags, mentions and URLs for a given tweet.
	emoticons = getemoticons(tweet)
	hashtags = gethashtags(tokenized_tweet)
	mentions = getmentions(tokenized_tweet)
	urls = geturls(tweet)

	# Get character n-grams (n=1-3) for a given tweet.
	char_n_grams = getcharngrams(tweet)

	stop_words = get_stop_words()
	# Replace emoticons, hashtags, mentions and URLs in a tweet.
	processed_tokenized_tweet = processtweet(tokenized_tweet, stop_words)
	processed_tweet = " ".join(processed_tokenized_tweet[0:])

	# Get word n-grams (n=1-5) for the tweet.
	word_n_grams = getwordngrams(processed_tokenized_tweet)

	return emoticons, hashtags, mentions, urls, char_n_grams, word_n_grams



# tweet = "En el día @shyamli de hoy #27óS sólo me @sahil sale del alma gritar ¡¡VIVA ESPAÑA! ! http://t.co/w9Bmsf4TUK :) (: #NLP"
