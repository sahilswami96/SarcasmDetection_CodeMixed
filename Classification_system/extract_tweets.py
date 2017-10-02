import string
import operator

fp = open("../Dataset/Sarcasm_tweets_with_language.txt", 'r')
id_tokenised_tweet_map = {}

tokens = []
for line in fp:
	line = line.strip()
	line = line.split(' ')
	line = [token.strip() for token in line if token != '' and token != ' ' and token != '\n']
	if len(line) == 0:
		id_tokenised_tweet_map[current_id] = tokens 
		tokens = []
	elif len(line) == 1:
		current_id = line[0]
	else:
		tokens.append(line[0])

if current_id not in id_tokenised_tweet_map:
	id_tokenised_tweet_map[current_id] = tokens

fp = open("../Dataset/Sarcasm_tweets.txt", 'r')
id_tweet_map = {}
tweet_id_map = {}
count = 0
for line in fp:
	line = line.strip()
	tokens = line.split(' ')
	if len(tokens) == 1 and tokens[0] != '':
		current_id = tokens[0]
	elif len(tokens) > 1:
		if current_id in id_tweet_map:
			print current_id
		id_tweet_map[current_id] = line
		tweet_id_map[line] = current_id
		count = count + 1

fp = open("../Dataset/Sarcasm_tweet_truth.txt", 'r')
id_truth_map = {}

for line in fp:
	line = line.strip()
	if line == '':
		continue
	elif line[0] in string.digits:
		current_id = line
	else:
		id_truth_map[current_id] = line

fp = open("../Dataset/Sarcasm_tweets_with_language.txt", 'r')
token_lang_map = {}

for line in fp:
	line = line.strip()
	line = line.split(' ')
	line = [token.strip() for token in line if token != '' and token != ' ' and token != '\n']
	if len(line) == 2:
		token_lang_map[line[0].lower()] = line[1].lower()

fp = open("../Dataset/Sarcasm_tweets_with_language.txt", 'r')
token_count = {}
stop_words = []

for line in fp:
	line = line.strip()
	line = line.split(' ')
	line = [token.strip() for token in line if token != '' and token != ' ' and token != '\n']
	if len(line) == 2:
		if line[0].lower() in token_count:
			token_count[line[0].lower()] += 1
		else:
			token_count[line[0].lower()] = 1
token_count = dict(sorted(token_count.items(), key=operator.itemgetter(1)))
for key, value in token_count.iteritems():
	if value >= 100:
		stop_words.append(key.lower())

def get_id_tokenised_tweet_map():
	return id_tokenised_tweet_map

def get_tweet_map():
	return id_tweet_map, tweet_id_map

def get_id_truth_map():
	return id_truth_map

def get_token_lang_map():
	return token_lang_map

def get_stop_words():
	return stop_words


# get_stop_words()