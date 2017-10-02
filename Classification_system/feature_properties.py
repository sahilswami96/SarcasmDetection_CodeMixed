#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import nltk
from extract_tweets import get_id_truth_map, get_tweet_map, get_id_tokenised_tweet_map, get_token_lang_map, get_stop_words
from preprocessing import gethashtags, getwordngrams, getcharngrams, processtweet

char_n_grams_index = {}
word_n_grams_index = {}

def getallcharngrams(id_tweet_map):
	char_n_grams = []
	n_grams_count = {}
	for key, tweet in id_tweet_map.iteritems():
		char_i_grams = getcharngrams(tweet)

		for i_gram in char_i_grams:
			if i_gram in n_grams_count:
				n_grams_count[i_gram] += 1
			else:
				n_grams_count[i_gram] = 1
	
	for i_gram, count in n_grams_count.iteritems():
		if count >= 8:
			char_n_grams.append(i_gram)
	return char_n_grams

def getcharngramsindex(char_n_grams):
	count = 0

	for i_gram in char_n_grams:
		char_n_grams_index[i_gram] = count
		count += 1

def getallwordngrams(id_tweet_map, id_tokenised_tweet_map):
	word_n_grams = []
	n_grams_count = {}
	for key, tweet in id_tweet_map.iteritems():
		tokenized_tweet = id_tokenised_tweet_map[key]
		word_i_grams = getwordngrams(tokenized_tweet)

		for i_gram in word_i_grams:
			if i_gram in n_grams_count:
				n_grams_count[i_gram] += 1
			else:
				n_grams_count[i_gram] = 1

	for i_gram, count in n_grams_count.iteritems():
		if count >= 10:
			word_n_grams.append(i_gram)
	return word_n_grams

def getwordngramsindex(word_n_grams):
	count = 0
	# print len(word_n_grams)
	for i_gram in word_n_grams:
		word_n_grams_index[i_gram] = count
		count += 1

def processtweetforwordngrams(id_tweet_map, id_tokenised_tweet_map):
	processed_id_tweet_map = {}
	processed_id_tokenised_tweet_map = {}
	stop_words = get_stop_words()
	for key, tweet in id_tweet_map.iteritems():
		tokenized_tweet = id_tokenised_tweet_map[key]
		
		# Replace emoticons, hashtags, mentions and URLs in a tweet and remove punctuations.
		processed_tokenized_tweet = processtweet(tokenized_tweet, stop_words)
		processed_tweet = " ".join(processed_tokenized_tweet[0:])

		processed_id_tweet_map[key] = processed_tweet
		processed_id_tokenised_tweet_map[key] = processed_tokenized_tweet

	return processed_id_tweet_map, processed_id_tokenised_tweet_map

def gettargethashtags(hashtag_count, hashtags, index_truth):
	for hashtag in hashtags:
		hashtag = hashtag.lower()
		if hashtag in hashtag_count[index_truth]:
			hashtag_count[index_truth][hashtag] += 1
		else:
			hashtag_count[index_truth][hashtag] = 1
	return hashtag_count

def gettargettokens(token_count, processed_tokenized_tweet, index_truth):
	for token in processed_tokenized_tweet:
		token = token.lower()
		if token in ['hashtag', 'url', 'mention', 'emoticon']:
			continue
		if token in token_count[index_truth]:
			token_count[index_truth][token] += 1
		else:
			token_count[index_truth][token] = 1
	return token_count

# Get count of all the hashtags and tokens for each of the class of gender and truth.
def gettargetwords(id_tweet_map, processed_id_tweet_map, id_tokenised_tweet_map, processed_id_tokenised_tweet_map, id_truth_map):
	hashtag_count = [{}, {}]
	token_count = [{}, {}]

	index = {}
	index['YES'] = 0
	index['NO'] = 1

	for key, tweet in id_tweet_map.iteritems():
		tokenized_tweet = id_tokenised_tweet_map[key]
		hashtags = gethashtags(tokenized_tweet)
		hashtag_count = gettargethashtags(hashtag_count, hashtags, index[id_truth_map[key]])

		processed_tokenized_tweet = processed_id_tokenised_tweet_map[key]
		token_count = gettargettokens(token_count, processed_tokenized_tweet, index[id_truth_map[key]])
	
	return token_count, hashtag_count

# Get hashtags with highest count for each of the class of gender and truth.
def gettophashtags(hashtag_count):
	truth_top_hashtags = []

	# Get hashtags for truth which have a score of >= 0.4.
	for i in xrange(0,2):
		for hashtag, value in hashtag_count[i].iteritems():
			c1 = float(value)
			total = 0.0
			if hashtag in hashtag_count[0]:
				total += float(hashtag_count[0][hashtag])
			if hashtag in hashtag_count[1]:
				total += float(hashtag_count[1][hashtag])
			
			if float(c1/total) >= 0.6 and total >= 5:
				truth_top_hashtags.append(hashtag)
	
	truth_top_hashtags = set(truth_top_hashtags)
	truth_top_hashtags = list(truth_top_hashtags)
	
	return truth_top_hashtags


def gettoptokens(token_count):
	truth_top_tokens = []

	# Get hashtags for gender which have a score of >= 0.4.
	for i in xrange(0,2):
		for token, value in token_count[i].iteritems():
			c1 = float(value)
			total = 0.0
			if token in token_count[0]:
				total += float(token_count[0][token])
			if token in token_count[1]:
				total += float(token_count[1][token])
			
			if float(c1/total) >= 0.6 and total >= 5:
				truth_top_tokens.append(token)
	
	token_lang_map = get_token_lang_map()

	truth_top_tokens = set(truth_top_tokens)
	truth_top_tokens = list(truth_top_tokens)

	truth_top_hi_tokens = []
	truth_top_en_tokens = []
	truth_top_rest_tokens = []

	for token in truth_top_tokens:
		if token.lower() not in token_lang_map:
			truth_top_rest_tokens.append(token)
		elif token_lang_map[token.lower()] == 'hi':
			truth_top_hi_tokens.append(token)
		elif token_lang_map[token.lower()] == 'en':
			truth_top_en_tokens.append(token)
		elif token_lang_map[token.lower()] == 'rest':
			truth_top_rest_tokens.append(token)
	
	return truth_top_hi_tokens, truth_top_en_tokens, truth_top_rest_tokens


def findfeatureproperties():
	id_tweet_map, tweet_id_map = get_tweet_map()
	id_tokenised_tweet_map = get_id_tokenised_tweet_map()
	id_truth_map = get_id_truth_map()

	# Get all char n-grams (n=1-5) from training set and create an index for each of them.
	char_n_grams = getallcharngrams(id_tweet_map)
	getcharngramsindex(char_n_grams)

	processed_id_tweet_map, processed_id_tokenised_tweet_map = processtweetforwordngrams(id_tweet_map, id_tokenised_tweet_map)

	# Get all word n-grams (n=1-3) from training set and create an index for each of them.
	word_n_grams = getallwordngrams(processed_id_tweet_map, processed_id_tokenised_tweet_map)
	getwordngramsindex(word_n_grams)

	token_count, hashtag_count = gettargetwords(id_tweet_map, processed_id_tweet_map, id_tokenised_tweet_map, processed_id_tokenised_tweet_map, id_truth_map)

	truth_top_hashtags = gettophashtags(hashtag_count)
	truth_top_hi_tokens, truth_top_en_tokens, truth_top_rest_tokens = gettoptokens(token_count)

	fp = open('data.txt', 'w')
	pickle.dump(6, fp)
	pickle.dump(char_n_grams_index, fp)
	pickle.dump(word_n_grams_index, fp)
	pickle.dump(truth_top_hashtags, fp)
	pickle.dump(truth_top_hi_tokens, fp)
	pickle.dump(truth_top_en_tokens, fp)
	pickle.dump(truth_top_rest_tokens, fp)
	fp.close()

	# return char_n_grams_index, word_n_grams_index, gender_top_hashtags, truth_top_hashtags, gender_top_tokens, truth_top_tokens


# findfeatureproperties()

			