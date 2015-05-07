
from nltk.corpus import stopwords
from porter_stemmer import PorterStemmer
import re
import string
from itertools import groupby

def tokenizer(text):
	word_tup_arr = {}
	word_arr = []

	# PARSING/PROCESSING ENTIRE TEXT
		# ---
	# [] replace newline characters
	text = text.replace('\r', ' ')
	text = text.replace('\n', ' ')
	# [] Lowercase
	text = text.lower()
	# [] Remove Punctuation
	text = punc_regex.sub('', text)

	words = text.split(" ")
	index = -1  #first index will be 0
	for word in words:
		index += 1
		# PARSING/PROCESSING SINLGE WORDS
		# ---
		# [] Stemming 
		word = stemmer.stem(word, 0, len(word)-1)
		# [] Remove Stopwords
		if word in stopwords_list:
			continue
		# [] Remove duplicate letters (up to 3)
		''.join(''.join(letter)[:3] for _, letter in groupby(word))
		# [] Remove short/long words
		if len(word) < 3 or len(word) > 20:
			continue
		# ADD TO WORD TUP LIST
		if word not in word_arr:
			word_arr.append(word)
			word_tup_arr[word] = []
		word_tup_arr[word].append(index)

	return word_tup_arr