#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import operator
import numpy as np
import preprocessing as pp

global char_n_grams_index, word_n_grams_index, truth_top_hashtags, truth_top_hi_tokens, truth_top_en_tokens, truth_top_rest_tokens
# Add features derived from emoticons.
def addemoticonfeatures(feature_vector, emoticons):
	feature_vector.append(len(emoticons))

	for i in xrange(len(pp.all_emoticons)):
		if pp.all_emoticons[i] in emoticons:
			feature_vector.append(1)
		else:
			feature_vector.append(0)
	return feature_vector

def addchargramfeatures(feature_vector, char_n_grams_index, char_n_grams):
	char_features = [0] * len(char_n_grams_index)
	for char_i_gram in char_n_grams:
		if char_i_gram in char_n_grams_index:
			char_features[char_n_grams_index[char_i_gram]] = 1
	feature_vector.extend(char_features)
	return feature_vector

def addwordfeatures(feature_vector, word_n_grams_index, word_n_grams):
	word_features = [0] * len(word_n_grams_index)

	for word_i_gram in word_n_grams:
		if word_i_gram in word_n_grams_index:
			word_features[word_n_grams_index[word_i_gram]] = 1
	feature_vector.extend(word_features)
	return feature_vector

def addtoptokenfeatures(feature_vector, top_hi_tokens, top_en_tokens, top_rest_tokens, tweet):
	for i in xrange(len(top_hi_tokens)):
		if top_hi_tokens[i].lower() in tweet.lower():
			feature_vector.append(1)
		else:
			feature_vector.append(0)
	for i in xrange(len(top_en_tokens)):
		if top_en_tokens[i].lower() in tweet.lower():
			feature_vector.append(1)
		else:
			feature_vector.append(0)
	for i in xrange(len(top_rest_tokens)):
		if top_rest_tokens[i].lower() in tweet.lower():
			feature_vector.append(1)
		else:
			feature_vector.append(0)
	return feature_vector

def buildtruthfeaturevector(key, tweet):
	global char_n_grams_index, word_n_grams_index, truth_top_hashtags, truth_top_hi_tokens, truth_top_en_tokens, truth_top_rest_tokens

	emoticons, hashtags, mentions, urls, char_n_grams, word_n_grams = pp.preprocess(key, tweet)

	truth_feature_vector = []

	truth_feature_vector = addemoticonfeatures(truth_feature_vector, emoticons)
	truth_feature_vector = addchargramfeatures(truth_feature_vector, char_n_grams_index, char_n_grams)
	truth_feature_vector = addwordfeatures(truth_feature_vector, word_n_grams_index, word_n_grams)
	truth_feature_vector = addtoptokenfeatures(truth_feature_vector, truth_top_hi_tokens, truth_top_en_tokens, truth_top_rest_tokens, tweet)
	return truth_feature_vector

# Build feature vector for a given tweet.
# 1. No. of emoticons and occurence for each emoticon.
# 2. Char n-grams (n=1-3).
# 3. Word n-grams (n=1-5).
# 4. Target tokens.
def getfeaturevector(key, tweet):
	global char_n_grams_index, word_n_grams_index, truth_top_hashtags, truth_top_hi_tokens, truth_top_en_tokens, truth_top_rest_tokens

	fp = open('data.txt', 'r')
	data = []
	for i in xrange(pickle.load(fp)):
		data.append(pickle.load(fp))
	char_n_grams_index, word_n_grams_index, truth_top_hashtags, truth_top_hi_tokens, truth_top_en_tokens, truth_top_rest_tokens = data
	truth_feature_vector = buildtruthfeaturevector(key, tweet)
	
	return truth_feature_vector

# tweet = "Tuits Tsunami! Optimistic about the future? #Elecciones #ComunicaciónPolítica #VamosJuntos #LlamadasQueUnen #CaminemosJuntos #Cambiemos #27S"
# getfeaturevector(tweet)
